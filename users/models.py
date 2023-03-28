from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """커스텀 유저 클래스"""

    pass

    ## 클래스 복수형 표현 수정 (or 다른 이름)
    class Meta:
        verbose_name_plural = "복수형/다른 이름"
