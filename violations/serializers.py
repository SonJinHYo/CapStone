from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import ViolationInfo, Violation



class ViolationInfoSerializer(ModelSerializer):
    """위반 관련 정보를 모두 보여주는 serializer"""

    violation_list = SerializerMethodField()
    region = SerializerMethodField()
    date = SerializerMethodField()
    
    def get_violation_list(self,obj):
        return [violation.name for violation in obj.violations.all()]
        
    def get_region(self,obj):
        return obj.cctv.region
    
    def get_date(self,obj):
        return obj.detected_time.date()
    
    class Meta:
        model = ViolationInfo
        fields = (
            "violation_list",
            "region",
            "img",
            "date",
        )
