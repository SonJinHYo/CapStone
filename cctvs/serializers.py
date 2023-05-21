from rest_framework.serializers import ModelSerializer
from .models import CCTV,ViolationFile


class CCTVSerializers(ModelSerializer):
    """기본 CCTV serializer"""

    class Meta:
        model = CCTV
        fields = "__all__"



class FileSerializer(ModelSerializer):
    class Meta:
        model = ViolationFile
        fiedls="__all__"