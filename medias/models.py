from django.db import models


class ViolationImage(models.Model):
    """Description ViolationsImage Class
    Properties:
        name (CharField) : 위반 사항
        region (ForeignKey-users.user) : 위반 지역
        detected_time (DateTimeField) : 위반 시간 (추후 변경 가능성 O)

    Descriptions:
        위반 이미지가 가진 정보
    """

    img = models.URLField(max_length=200)
    region = models.ForeignKey(
        "regions.Region",
        on_delete=models.CASCADE,
        related_name="violationimages",
    )
    detected_time = models.DateTimeField(auto_now=False)  # 이후 수정 필요 (감지 시간을 언제로 받을지)
    violation_infos = models.ManyToManyField(
        "medias.ViolationInfo",
        related_name="violationimages",
    )


class ViolationInfo(models.Model):
    """Description ViolationsImage Class
    Properties:
        img (URLField) : 위반 내용이 담긴 사진 (CloudFlare에 저장된 URL을 불러올 예정)
        name (CharField) : 위반 사항
        descriptions (TextField) : 위반 사유

    Descriptions:
        이미지에서 검출 가능한 위반 정보.
    """

    img = models.ForeignKey(
        "medias.ViolationImage",
        on_delete=models.CASCADE,
        related_name="violationinfos",
    )
    name = models.CharField(max_length=50)
    region = models.ForeignKey(
        "regions.Region",
        on_delete=models.CASCADE,
        related_name="violationimages",
    )
    detected_time = models.DateTimeField(
        auto_now=False
    )  # 이후 수정 필요 (감지 시간을 언제로 받을지 / DateField? DateTimeField?)
    descriptions = models.TextField(max_length=1000)
