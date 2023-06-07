from django.db import transaction
from django.contrib import admin

from rest_framework import exceptions

from .models import CCTV,ViolationFile
from violations.models import ViolationInfo,Violation
from violations.serializers import ViolationInfoSerializer
from cctvs.models import CCTV

import shutil
import boto3
import zipfile
import os

from PIL import Image

s3 = boto3.client('s3')

@admin.register(CCTV)
class CCTVAdmin(admin.ModelAdmin):
    """CCTV class를 관리"""

    list_display = (
        "name",
        "region",
        "description",
    )

def save_and_get_gif_address(image_dir:str) -> str:
    """ 이미지 폴더 위치를 받아서 gif로 변환하는 함수
    Args:
        image_dir (str) : 이미지의 폴더 주소
        gif_address (str) : gif 이미지의 주소
        filename (str) : 이미지파일명 (ex. 0_0_114.jpg)
    Return:
        None
    """
    images = []
    for filename in os.listdir(image_dir):
        image_path = os.path.join(image_dir,filename)
        image = Image.open(image_path)
        images.append(image)
        gif_address = f"/srv/QuitBoard_Backend/tmp/gif/{filename[:-4]}.gif"
        
        images[0].save(gif_address, save_all=True, append_images=images[1:], duration=100, loop=0)
            
    return gif_address

def save_violation_data(dir_name:str,region:str,text:str) -> None:
    """ DB에 위반정보를 저장하는 함수
    Args:
        dir_name (str) : 위반이미지의 폴더명
        region (str) : 위반 지역
        text (str) : 위반 사항과 위반 시간을 담은 문자열 (ex. text = 0010,2023-04-23T15:45:43)
        violation_list (list) : 현재 저장된 위반 사항
        violations,time (str) : text를 , 기준으로 나누어 위반 사항과 시간을 저장한 변수
        v_set (set) : 위반 사항을 전부 담은 집합
        image_name (str) : 이미지는 filename과 같은 이름으로 확장자만 png로 다르기 때문에 filename의 확장자면 변경하여 image_name으로 저장한 변수
        image_time (str) : DB에는 초단위까지 시간을 저장하지만 S3폴더에 일자별로 저장하기 위해 년월일 단위까지 따로 일자를 저장
        bucket,key (str) : 버킷 이름, 하위 위치
        v (django_Model_object) : DB에 저장할 django모델 객체
        
    Return:
        None
        
    """

    violation_list = [obj.name for obj in Violation.objects.all()]
    violations,time = text.split(',')
    v_set = {violation_list[idx] for idx,i in enumerate(violations) if i=='1'}
    
    image_time = time[:time.find('T')]
    gif_name = save_and_get_gif_address(f'/srv/QuitBoard_Backend/tmp/images/{dir_name}')
    bucket,key = 'quit-board-bucket', f'images/{image_time}/{dir_name}.gif'
		
	# home경로의 aws key를 통해 s3버킷에 파일 업로드
    s3.upload_file(Filename=gif_name, Bucket=bucket, Key=key)

    # 업로드한 파일의 이미지 경로를 포함하여 위반객체(ViolationaInfo) 생성 후 One-to-Many관계(Violation-ViolationInfo) 추가
    v = ViolationInfo.objects.create(
        cctv = CCTV.objects.get(region=region),
        detected_time = time,
        img = f'https://{bucket}.s3.ap-northeast-2.amazonaws.com/{key}',
    )
    v.violations.set([obj for obj in Violation.objects.all() if obj.name in v_set])
    
    return None
  
# def save_violation_data(filename,region,text):
#     """ DB에 위반정보를 저장하는 함수
#     Args:
#         filename (str) : 확장자를 포함한 파일의 이름
#         region (str) : 위반 지역
#         text (str) : 위반 사항과 위반 시간을 담은 문자열 (ex. text = 0010,2023-04-23T15:45:43)
#         violation_list (list) : 현재 저장된 위반 사항
#         violations,time (str) : text를 , 기준으로 나누어 위반 사항과 시간을 저장한 변수
#         v_set (set) : 위반 사항을 전부 담은 집합
#         image_name (str) : 이미지는 filename과 같은 이름으로 확장자만 png로 다르기 때문에 filename의 확장자면 변경하여 image_name으로 저장한 변수
#         image_time (str) : DB에는 초단위까지 시간을 저장하지만 S3폴더에 일자별로 저장하기 위해 년월일 단위까지 따로 일자를 저장
#         bucket,key (str) : 버킷 이름, 하위 위치
#         v (django_Model_object) : DB에 저장할 django모델 객체
        
#     Return:
#         None
        
#     """

#     violation_list = [obj.name for obj in Violation.objects.all()]
#     violations,time = text.split(',')
#     v_set = {violation_list[idx] for idx,i in enumerate(violations) if i=='1'}
    
#     image_name,image_time = f'{filename[:-4]}.png',time[:time.find('T')]
#     bucket,key = 'quit-board-bucket', f'images/{image_time}/{image_name}'
		
# 		# home경로의 aws key를 통해 s3버킷에 파일 업로드
#     s3.upload_file(Filename=f'/srv/QuitBoard_Backend/tmp/images/{image_name}', Bucket=bucket, Key=key)

#     # 업로드한 파일의 이미지 경로를 포함하여 위반객체(ViolationaInfo) 생성 후 One-to-Many관계(Violation-ViolationInfo) 추가
#     v = ViolationInfo.objects.create(
#         cctv = CCTV.objects.get(region=region),
#         detected_time = time,
#         img = f'https://{bucket}.s3.ap-northeast-2.amazonaws.com/{key}',
#     )
#     v.violations.set([obj for obj in Violation.objects.all() if obj.name in v_set])
    
#     return None

@admin.action(description="zip파일 업데이트 후 삭제")
def update_violations_data(ViolationFileAdmin, request, violation_files):
    """ zip파일 압축 해제 후 파싱하여 데이터를 저장하는 함수
    
    Args:
        ViolationFileAdmin (class) : 관리 객체
        request (dict) : request 정보
        violation_files (class) : 관리창에서 선택한 객체 쿼리. (zip 파일들)
        vio_dir = 압축 해제 후 위반 정보가 저장된 폴더의 위치
    
    Returns:
        None
    """
    try:
        with transaction.atomic():
			# 선택된 zip파일 전체 조회
            for violation_file in violation_files.all():
				# zip파일의 압축을 임시폴더로 "./tmp"에 풀어 위반 정보 조회
                with violation_file.file.open() as zip_content:
                    with zipfile.ZipFile(zip_content,'r') as zip_ref:
                        zip_ref.extractall('/srv/QuitBoard_Backend/tmp')
                    vio_dir = '/srv/QuitBoard_Backend/tmp/violations'
                    for filename in os.listdir(vio_dir):
                        with open(os.path.join(vio_dir, filename), 'r') as f:
                            content = f.read()
							# 위반 사항이 있는 데이터는 데이터 저장 함수를 통해 저장
                            if int(content[:content.find(',')]) != 0:
                                # save_violation_data(filename,violation_file.cctv.region,content)
                                save_violation_data(filename[:-4],violation_file.cctv.region,content)
					# 조회가 끝나면 임시 폴더 삭제
                    shutil.rmtree('/srv/QuitBoard_Backend/tmp')
				# 업데이트가 끝난 데이터를 다시 조회하지 않도록 객체 삭제
                violation_file.delete()
        return None
    except Exception:
        raise exceptions.ParseError

@admin.register(ViolationFile)
class ViolationFileAdmin(admin.ModelAdmin):
    actions = [update_violations_data,]
    list_display = (
        "file",
        "cctv", 
    )
