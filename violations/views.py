from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
from .models import ViolationInfo

from collections import defaultdict


class AllViolations(APIView):
    """descriptions ALLViolations Class

    return:
        data (dict): 위반 횟수를 센 정보를 합친 딕셔너리
        data["violationCountObj"] (dict) : 각 규정별 위반 횟수
        data["regionCountObj"] (dict) : 각 구역별 위반 횟수
        data["detectedHourCountObj"] (dict) : 각 시간대별 위반 횟수 (감지된 시간의 hour만 측정)

    Description:
        전체 현황을 요약하여 보여주기 위한 view클래스.
    """

    def get(self, request):
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
