from django.db import models


# Create your models here.
class CCTV(models.Model):
    """CCTV Model Description

    Fields
        name (CharField) : 모델명
        law (CharField) : 위반 사항에 대한 법률
    """

    name = models.CharField(
        max_length=50,
        verbose_name="모델명",
    )
    region = models.ForeignKey(
        "cctvs.Region",
        verbose_name="설치지역",
        on_delete=models.SET_NULL,
        null=True,
    )


class Region(models.Model):
    """Region Model Description

    Fields
        name (CharField) : 지역명
        description (TextField) : 상세주소
    """

    name = models.CharField(
        max_length=50,
        verbose_name="지역명",
    )
    description = models.TextField(
        verbose_name="상세 주소",
    )
