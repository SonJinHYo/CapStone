from django.db import models


class ViolationInfo(models.Model):
    """Violation Model Description

    Fields:
        name (ManyToManyField) : 위반 사항
        img () : 위반당시 이미지
        region : 위반
    Descriptions:
        위반정보를 전부 모은 모델. 하나의 오브젝트가 하나의 위반데이터를 가진다.
    """

    name = models.ManyToManyField(
        "violations.Violation",
        related_name="v_info",
    )
    img = models.ForeignKey(
        "medias.Photo",
        on_delete=models.CASCADE,
        related_name="v_info",
    )
    cctv = models.ForeignKey(
        "cctvs.CCTV",
        on_delete=models.SET_NULL,
        related_name="v_info",
        null=True,
    )


class Violation(models.Model):
    """Violation Model Description

    Fields
        name (CharField) : 위반 사항
        law (CharField) : 위반 사항에 대한 법률
    """

    name = models.CharField(max_length=50)
    law = models.TextField()
