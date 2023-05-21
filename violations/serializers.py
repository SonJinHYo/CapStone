from rest_framework.serializers import ModelSerializer,SerializerMethodField
from cctvs.serializers import TinyCCTVSerializer
from .models import ViolationInfo, Violation



class TinyViolationSerializer(ModelSerializer):
    """api/v1/service (전체현황요약 페이지) 에 사용할 위반사항 serializer"""
    class Meta:
        model = Violation
        fields = ("name",)


class ViolationInfoSerializer(ModelSerializer):
    """위반 관련 정보를 모두 보여주는 serializer"""

    violation_list = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    
    def get_violation_list(self,ViolationInfo):
        return ', '.join([violation.name for violation in ViolationInfo.violations.objects.all()])
        
    def get_region(self,ViolationInfo):
        return ViolationInfo.cctv.region
    
    class Meta:
        model = ViolationInfo
        fields = (
            "violation_list",
            "region",
            "img",
            "detected_time",
        )
