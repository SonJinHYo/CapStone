from rest_framework.serializers import ModelSerializer
from .models import ViolationInfo


class TinyViolationSerializer(ModelSerializer):
    """api/v1/service 페이지의 전체 현황 요약에 보일 ViolationInfo 필드"""

    class Meta:
        model = ViolationInfo
        fields = "__all__"
