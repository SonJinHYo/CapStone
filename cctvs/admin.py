from django.contrib import admin
from .models import CCTV,ViolationFile
from violations.models import ViolationInfo
from violations.serializers import ViolationInfoSerializer


@admin.register(CCTV)
class CCTVAdmin(admin.ModelAdmin):
    """CCTV class를 관리"""

    list_display = (
        "name",
        "region",
        "description",
    )


def upload_video(video_address):
    """영상을 입력하면 분할이미지와 그 정보를 반환하는 함수 (임시)

    Args:
        video_address (str): cctv 영상 주소
    return:
        image_info (list(dict)): 딕셔너리를 원소로 가지는 리스트
            (dict) : {
                img: (str: 위반이미지 주소),
                violations: (list(str): 분류된 위반 사항 목록)
                cctv: (str: cctv 위치)
                detected_time : (str: 위반 당시 시간)
            }
    """

    pass
    return list()


@admin.action(description="S3 버킷의 데이터 불러오기")
def upload_zip_file(model_admin, request, videos):
    
    for video in videos.all():
        # 업로드가 안된 객체만 수행
        if not video.upload:
            # upload_video 함수에서 위반 정보들을 받아온다.
            for violation_info in upload_video(video_address="video_address"):
                # 위반 정보가 객체 정보에 들어맞다면 저장
                serializer = ViolationInfoSerializer(data=violation_info)
                if serializer.is_valid():
                    serializer.save()
            video.upload = True
            video.save()


@admin.register(ViolationFile)
class ViolationFileAdmin(admin.ModelAdmin):
    actions = (upload_zip_file,)
    list_display = (
        "file",
        "cctv",
    )
