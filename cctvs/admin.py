from django.db import transaction
from django.contrib import admin

from rest_framework import exceptions

from .models import CCTV, ViolationFile
from cctvs.models import CCTV
from .tasks import task_rm_zip, task_save_violation_data

import zipfile
import os


@admin.register(CCTV)
class CCTVAdmin(admin.ModelAdmin):
    """CCTV class를 관리"""

    list_display = (
        "name",
        "region",
        "description",
    )


@admin.action(description="zip파일 업데이트 후 삭제")
def update_violations_data(ViolationFileAdmin, request, violation_files):
    """zip파일 압축 해제 후 파싱하여 데이터를 저장하는 함수

    Args:
        ViolationFileAdmin (class) : 관리 객체
        request (dict) : request 정보
        violation_files (class) : 관리창에서 선택한 객체 쿼리. (zip 파일들)
        vio_dir = 압축 해제 후 위반 정보가 저장된 폴더의 위치

    Returns:
        None
    """

    try:
        ViolationFileAdmin.message_user(request, "업데이트를 시작합니다.")
        with transaction.atomic():
            # 선택된 zip파일 전체 조회
            for violation_file in violation_files.all():
                # zip파일의 압축을 임시폴더로 "./tmp"에 풀어 위반 정보 조회
                with violation_file.file.open() as zip_content:
                    with zipfile.ZipFile(zip_content, "r") as zip_ref:
                        zip_ref.extractall("/srv/QuitBoard_Backend/tmp")
                    vio_dir = "/srv/QuitBoard_Backend/tmp/violations"
                    for filename in os.listdir(vio_dir):
                        with open(os.path.join(vio_dir, filename), "r") as f:
                            content = f.read()
                            # 위반 사항이 있는 데이터는 데이터 저장 함수를 통해 저장
                            if int(content[: content.find(",")]) != 0:
                                task_save_violation_data.delay(
                                    filename[:-4],
                                    violation_file.cctv.region,
                                    content,
                                )
                    # 조회가 끝나면 임시 폴더 삭제
                    task_rm_zip.delay("/srv/QuitBoard_Backend/tmp")
        # 업데이트가 끝난 데이터를 다시 조회하지 않도록 객체 삭제
        violation_file.delete()
        # task_admin_message(request, "파일 업데이트를 완료하였습니다.")

        return None
    except Exception:
        raise exceptions.ParseError


@admin.register(ViolationFile)
class ViolationFileAdmin(admin.ModelAdmin):
    actions = [
        update_violations_data,
    ]
    list_display = (
        "file",
        "cctv",
    )
