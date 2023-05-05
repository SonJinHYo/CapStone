import os
import boto3
import environ

from django.db import models


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
        
class S3Uploader:
    env = environ.Env()
    
    def __init__(self, file):
        self.file = file

    def upload(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id     = env("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key = env("AWS_SECRET_ACCESS_KEY")
        )
        url = 'zip_dir'+'/'+uuid.uuid1().hex
        
        s3_client.upload_fileobj(
            self.file, 
            env("AWS_STORAGE_BUCKET_NAME"), 
            url, 
            ExtraArgs={
                "ContentType": self.file.content_type
            }
        )
        return url

def custom_upload_to(instance, filename):
    uploader = S3Uploader(instance)
    url = uploader.upload()
    return os.path.join("media/cctv", instance.cctv.name, filename)


class ViolationFile(models.Model):
    """Video Model Description

    Field:
        file (FileField) : 위반 데이터를 zip으로 받는 필드. 딥러닝 모델을 거쳐 위반 이미지만 db에 저장할 예정
    """

    # 임시 함수. 후에 딥러닝 모델과 결합 후 위치,내용 재정의

    file = models.FileField(
        upload_to=custom_upload_to,
        max_length=100,
    )

    cctv = models.ForeignKey(
        "cctvs.CCTV",
        verbose_name="CCTV",
        on_delete=models.SET_NULL,
        related_name="videos",
        null=True,
    )


    def __str__(self) -> str:
        return f"{self.cctv.name}/{self.file.name}"

