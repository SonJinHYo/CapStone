from django.utils import timezone
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.core.cache import cache

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .serializers import ViolationInfoSerializer
from .models import ViolationInfo, Violation
from cctvs.models import CCTV
from collections import defaultdict

class AllViolations(APIView):
    """AllViolations APIView

    ViolationInfo 모델을 사용하여 각 위반 유형, 지역 및 감지 시간별로 계수를 반환하는 API end point.

    Method:
        get(request)

    Attributes:
        None
    """

    def get(self, request):
        """
        모든 위반 정보에서 감지된 위반의 수, 각 지역에서 감지된 위반의 수,
        감지된 시간대별 위반의 수를 포함하는 JSON 반환.

        Returns:
            JSON:
                - violationCountObj (_dict_): 위반 정보별 위반 횟수
                - regionCountObj (_dict_): 각 지역별 위반 횟수
                - detectedHourCountObj (_dict_): 시간대(시 단윈)별 위반 횟수
        """
        today = DateFormat(datetime.now()).format('Ymd')
        data = cache.get(today)
        if data is None:
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
            cache.set(today,data,60*30)

        return Response(
            data,
            status=HTTP_200_OK,
        )


class ViolationDetail(APIView):
    """ViolationDetail APIView

        요청받은 조건을 만족하는 위반 정보를 자세하게 모두 보내는 API end point.

    Method:
        get(request,kind,detail)
        validate_date(date_text)
    Attributes:
        None
    """

    def valid_date_input(self, date_text):
        """유효 날짜 확인 함수

        Args:
            date_text (str): ex. "2023_02_22"

        Returns:
            boolean : _
        """

        try:
            result = timezone.datetime.strptime(date_text, "%Y-%m-%d") 
            return True
        except ValueError:
            return False

    def get(self, request, kind, detail):
        """
        kind과 detail를 기반으로 위반사항, 지역, 날짜 정보에 따른 위반 정보를 반환.

        Parameters:
            - request: HTTP 요청
            - kind (_str_) : "violation", "region", "time" 중 하나로 선택됩.
            - detail (_str_) : kind에 따라 위반사항의 이름, 지역 이름, 날짜 정보 중 하나로 선택.

        Returns:
            - Response: 해당 요청에 따른 위반 정보가 담긴 JSON 형식의 데이터를 반환.
        """

        if kind == "violation":  # detail : 위반사항
            serializer = ViolationInfoSerializer(
                ViolationInfo.objects.filter(violations__name__contains=detail),
                many=True,
            )
            return Response(data=serializer.data, status=HTTP_200_OK)

        elif kind == "region":  # detail : 지역
            serializer = ViolationInfoSerializer(
                ViolationInfo.objects.filter(cctv__region=detail),
                many=True,
            )
            return Response(data=serializer.data, status=HTTP_200_OK)

        elif kind == "time":  # detail : 연-월-일
            # DB를 살펴볼 필요가 없은 예외
            # 3개의 입력이 아니고, 연/월/일 입력이 유효하지 않은 날짜일 때,
            if not self.valid_date_input(detail):
                return Response(status=HTTP_400_BAD_REQUEST)

            year, month, day = detail.split("-")

            serializer = ViolationInfoSerializer(
                ViolationInfo.objects.filter(
                    detected_time__year=year,
                    detected_time__month=month,
                    detected_time__day=day,
                ),
                many=True,
            )
            return Response(data=serializer.data, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)


class Choice(APIView):
    """Choice APIView

    POST 요청에 따라 반환할 데이터를 결정하는 API end point.

    Method:
        get(request): GET 요청에 따라 해당 존재하는 데이터를 제공.

    Attribute:
        None
    """

    def get(self, request, kind):
        """
        POST 요청을 처리하고, 요청 데이터의 'kind'(선택한 필터 종류) 따라 다른 Response를 반환.

        """
        if kind == "violation":
            response_data = [violation.name for violation in Violation.objects.all()]
            return Response(response_data, status=HTTP_200_OK)

        elif kind == "region":
            response_data = [cctv.region for cctv in CCTV.objects.all()]
            return Response(response_data, status=HTTP_200_OK)

        elif kind == "time":
            return Response(status=HTTP_200_OK)

        else:
            return Response(status=HTTP_400_BAD_REQUEST)
