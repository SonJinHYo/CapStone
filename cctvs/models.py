import os
import boto3
import environ

from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class CCTV(models.Model):
    """CCTV Model Description

    Fields:
        name (CharField) : 모델명
        region (CharField) : 설치 지역
        description (TextField) : 상세 주소 및 추가 설명
    """

    name = models.CharField(
        max_length=50,
        verbose_name="모델명",
    )
    region = models.CharField(
        max_length=50,
        verbose_name="감시 지역",
    )
    description = models.TextField(
        verbose_name="상세 주소 / 추가 설명",
        blank=True,
    )

    def __str__(self) -> str:
        if len(self.description) > 15:
            return f"{self.region} / {self.description[:15]}..."
        else:
            return f"{self.region} / {self.description}"

    class Meta:
        verbose_name_plural = "CCTV 관리"


class ViolationFile(models.Model):
    """Video Model Description

    Field:
        file (FileField) : 위반 데이터를 zip으로 받는 필드. 딥러닝 모델을 거쳐 위반 이미지만 db에 저장할 예정
    """

    file = models.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["zip"])],
        help_text=f"zip을 업로드하세요. zip파일 구조는 다음과 같아야 합니다. <br/>\
        - filename.zip<br/>\
          &nbsp&nbsp&nbsp&nbsp- violations<br/>\
          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 1.txt<br/>\
          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 2.txt<br/>\
          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp:<br/>\
          &nbsp&nbsp&nbsp&nbsp- images<br/>\
          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 1.png<br/>\
          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp- 2.png<br/>\
          &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp &nbsp&nbsp&nbsp&nbsp:",
    )

    cctv = models.ForeignKey(
        "cctvs.CCTV",
        verbose_name="CCTV",
        on_delete=models.CASCADE,
        related_name="videos",
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.cctv.region}"

    class Meta:
        verbose_name_plural = "CCTV 영상 업로드"
