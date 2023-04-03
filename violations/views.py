from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .serializers import ViolationInfoSerializer
from .models import ViolationInfo, Violation
from cctvs.models import CCTV

from collections import defaultdict
import json


class AllViolations(APIView):
    """AllViolations APIView

    ViolationInfo 모델을 사용하여 각 위반 유형, 지역 및 감지 시간별로 계수를 반환하는 API end point.

    Methods:
        get(request): 위반 유형, 지역 및 감지 시간별로 개수를 검색하고 dict 형식으로 반환합니다.
            Response:

    Attributes:
        None
    """

    def get(self, request):
        """
        Args:
            request.data : None

        Returns:
            _dict_ : 각 위반사항 갯수 반환

        example:
            {
                "violationCountObj": {
                    "<violation 1>": <count>,
                    "<violation 2>": <count>,
                    ...
                },
                "regionCountObj": {
                    "<region 1>": <count>,
                    "<region 2>": <count>,
                    ...
                },
                "detectedHourCountObj": {
                    "<hour 1>": <count>,
                    "<hour 2>": <count>,
                    ...
                }
            }

        """
        violation_cnt, region_cnt, detected_hour_cnt = (
            defaultdict(int),
            defaultdict(int),
            defaultdict(int),
        )

        for violation_info in ViolationInfo.objects.all():
            for violation in violation_info.__str__().split(","):
                violation_cnt[violation] += 1
            region_cnt[violation_info.cctv.region] += 1
            detected_hour_cnt[violation_info.detected_time.hour] += 1

        data = {
            "violationCountObj": violation_cnt,
            "regionCountObj": region_cnt,
            "detectedHourCountObj": detected_hour_cnt,
        }

        return Response(
            data,
            status=HTTP_200_OK,
        )


class ViolationDetail(APIView):
    def get(self, request, choice1, choice2):
        if choice1 not in {"violation", "region", "time"}:
            return Response(status=HTTP_400_BAD_REQUEST)

        if choice1 == "violation":  # choice2 : 위반사항
            serializer = ViolationInfoSerializer(
                ViolationInfo.objects.filter(violations__name__contains=choice2),
                many=True,
            )
            return Response(data=serializer.data, status=HTTP_200_OK)

        elif choice1 == "region":  # choice2 : 지역
            cctv = CCTV.objects.get(region=choice2)
            serializer = ViolationInfoSerializer(
                ViolationInfo.objects.filter(cctv=cctv),
                many=True,
            )
        elif choice1 == "time":  # choice2 : 연/월/일
            year, month, day = choice2.split("/")
            serializer = ViolationInfoSerializer(
                ViolationInfo.objects.filter(
                    detected_time__year=year,
                    detected_time__month=month,
                    detected_time__day=day,
                ),
                many=True,
            )
            return Response(data=serializer.data, status=HTTP_200_OK)


class Choice(APIView):
    """Choice APIView

    POST 요청에 따라 반환할 데이터를 결정하는 API end point.

    Method:
        get(request): HTTP_200_OK 상태로 response.
        post(request): POST 요청에 따라 해당 존재하는 데이터를 제공.

    Attribute:
        None
    """

    def get(self, request):
        return Response(status=HTTP_200_OK)

    def post(self, request):
        data = request.data
        if data["kind"] == "violation":
            response_data = [violation.name for violation in Violation.objects.all()]
            return Response(response_data, status=HTTP_200_OK)

        elif data["kind"] == "region":
            response_data = [cctv.region for cctv in CCTV.objects.all()]
            return Response(response_data, status=HTTP_200_OK)

        elif data["kind"] == "time":
            return Response(status=HTTP_200_OK)

        else:
            return Response(status=HTTP_400_BAD_REQUEST)
