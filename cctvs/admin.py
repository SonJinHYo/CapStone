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

@admin.register(ViolationFile)
class ViolationFileAdmin(admin.ModelAdmin):
    list_display = (
        "file",
        "cctv", 
    )
