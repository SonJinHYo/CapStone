from django.db import models


class ViolationInfo(models.Model):
    """Violation Model Description

    Fields:
        violations (ManyToManyField) : 위반 사항들
        img (URLField) : 위반당시 이미지 주소
        cctv : 위반 이미지를 찍은 cctv 위치
        detected_time (DateTimeField) : 위반 당시 시간

    Descriptions:
        위반정보를 전부 모은 모델. 하나의 오브젝트가 하나의 위반데이터를 가진다.
    """

    violations = models.ManyToManyField(
        "violations.Violation",
        related_name="v_info",
    )
    img = models.URLField(max_length=300, verbose_name="이미지 URL")
    cctv = models.ForeignKey(
        "cctvs.CCTV",
        on_delete=models.SET_NULL,
        related_name="v_info",
        null=True,
    )
    detected_time = models.DateTimeField(
        auto_now=False
    )  # 이후 수정 필요 (감지 시간을 언제로 받을지 / DateField? DateTimeField?)

    def __str__(self) -> str:
        return ",".join([violation.name for violation in self.violations.all()])

    class Meta:
        verbose_name_plural = "규정 위반 데이터 관리"


class Violation(models.Model):
    """Violation Model Description

    Fields
        name (CharField) : 위반 사항
        law (CharField) : 위반 사항에 대한 법률
    """

    name = models.CharField(max_length=50)
    law = models.TextField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "위반규정 관리"
