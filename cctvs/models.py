from django.db import models


# Create your models here.
class CCTV(models.Model):
    """CCTV Model Description

    Fields
        name (CharField) : 모델명
        region (CharField) : 설치 지역
        description (TextField) : 상세 주소 및 추가 설명
    """

    class Meta:
        verbose_name_plural = "CCTVs"

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
