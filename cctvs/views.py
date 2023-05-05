from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileSerializer
from rest_framework import status

class Upload(APIView):
    def post(self,request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer
            