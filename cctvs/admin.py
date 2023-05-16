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
import io

s3 = boto3.client('s3')

@admin.register(CCTV)
class CCTVAdmin(admin.ModelAdmin):
    """CCTV class를 관리"""

    list_display = (
        "name",
        "region",
        "description",
    )
    
def save_violation_data(filename,region,s):  
    violation_list = [obj.name for obj in Violation.objects.all()]
    violations,time = s.split(',')
    v_list = {violation_list[idx] for idx,i in enumerate(violations) if i=='1'}
    
    image_name,image_time = f'{filename[:-4]}.png',time[:time.find('T')]
    bucket,key = 'quit-board-bucket', f'images/{image_time}/{image_name}'
    s3.upload_file(Filename=f'/srv/QuitBoard_Backend/tmp/images/{image_name}', Bucket=bucket, Key=key)
    
    v = ViolationInfo.objects.create(
        cctv = CCTV.objects.get(region=region),
        detected_time = time,
        img = f'https://{bucket}.s3.ap-northeast-2.amazonaws.com/{key}',
    )
    v.violations.set([obj for obj in Violation.objects.all() if obj.name in v_list])
    
    return None

@admin.action(description="zip파일 업데이트 후 삭제")
def update_violations_data(ViolationFileAdmin, request, violation_files):
    try:
        with transaction.atomic():
            for violation_file in violation_files.all():
                with violation_file.file.open() as zip_content:
                    with zipfile.ZipFile(zip_content,'r') as zip_ref:
                        zip_ref.extractall('/srv/QuitBoard_Backend/tmp')
                    vio_dir = '/srv/QuitBoard_Backend/tmp/violations'
                    for filename in os.listdir(vio_dir):
                        with open(os.path.join(vio_dir, filename), 'r') as f:
                            content = f.read()
                            if int(content[:content.find(',')]) != 0:
                                save_violation_data(filename,violation_file.cctv.region,content)
                    shutil.rmtree('/srv/QuitBoard_Backend/tmp')
                violation_file.delete()
    except Exception:
        raise exceptions.ParseError

@admin.register(ViolationFile)
class ViolationFileAdmin(admin.ModelAdmin):
    actions = [update_violations_data,]
    list_display = (
        "file",
        "cctv", 
    )
