from rest_framework.serializers import ModelSerializer
from .models import CCTV


class CCTVSerializers(ModelSerializer):
    """기본 CCTV serializer"""

    class Meta:
        model = CCTV
        fields = "__all__"


class TinyCCTVSerializer(ModelSerializer):
    """api/v1/service (전체현황요약 페이지) 에 사용할 CCTV serializer"""

    class Meta:
        model = CCTV
        fields = ("region",)
