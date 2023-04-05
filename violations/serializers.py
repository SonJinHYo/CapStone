from rest_framework.serializers import ModelSerializer
from cctvs.serializers import TinyCCTVSerializer
from .models import ViolationInfo, Violation


class TinyViolationSerializer(ModelSerializer):
    """api/v1/service (전체현황요약 페이지) 에 사용할 위반사항 serializer"""

    class Meta:
        model = Violation
        fields = ("name",)


class ViolationInfoSerializer(ModelSerializer):
    """위반 관련 정보를 모두 보여주는 serializer"""

    violations = TinyViolationSerializer(read_only=True, many=True)
    cctv = TinyCCTVSerializer(read_only=True)

    class Meta:
        model = ViolationInfo
        fields = (
            "violations",
            "cctv",
            "img",
            "detected_time",
        )
