from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .serializers import TinyViolationSerializer
from .models import ViolationInfo


class AllViolations(APIView):
    def get(self, request):
        serializer = TinyViolationSerializer(ViolationInfo.objects.all(), many=True)
        return Response(serializer.data, status=HTTP_200_OK)
