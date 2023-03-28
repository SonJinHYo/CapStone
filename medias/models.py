from django.db import models


class Photo(models.Model):
    """Description Photo Class
    Fields:
        detected_time (DateTimeField) : 위반 당시 시간

    Descriptions:
        이미지 데이터. 위반 관련 정보는 violations app으로 저장될 예정
    """

    detected_time = models.DateTimeField(
        auto_now=False
    )  # 이후 수정 필요 (감지 시간을 언제로 받을지 / DateField? DateTimeField?)
