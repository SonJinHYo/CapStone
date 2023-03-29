import datetime

from django.utils import timezone

from rest_framework.test import APITestCase
from .models import Violation, ViolationInfo
from cctvs.models import CCTV


class TestALLViolations(APITestCase):
    """ALLViolations Class Test"""

    VIO1, VIO2, WRONG_VIO = "2인 이상 탑승", "헬멧 미착용", "없음"
    LAW1, LAW2 = "law1", "law2"
    IMG_URL = "abcd"
    DETECTED_TIME = timezone.now()
    CCTV_NAME = "A1"
    CCTV_REGION = "자연대3호관"
    CCTV_DESC = "뒷문 주차장"

    def create_violations(self, violation_name, law_name):
        """
        위반규정 생성
        """
        data = {
            "name": violation_name,
            "law": law_name,
        }
        return Violation.objects.create(**data)

    def create_cctv(self):
        """
        cctv object 생성
        """
        data = {
            "name": self.CCTV_NAME,
            "region": self.CCTV_REGION,
            "description": self.CCTV_DESC,
        }
        return CCTV.objects.create(**data)

    def create_violation_info_1(self):
        """
        위반 규정이 1개인 ViolationInfo object 생성
        """
        v1 = self.create_violations(self.VIO1, self.LAW1)
        data = {
            "img": self.IMG_URL,
            "detected_time": self.DETECTED_TIME,
        }
        v_info1 = ViolationInfo.objects.create(**data)
        v_info1.violations.add(v1)
        return v_info1

    def create_violation_info_2(self):
        """
        위반 규정이 1개인 ViolationInfo object 생성
        """
        v1 = self.create_violations(self.VIO1, self.LAW1)
        v2 = self.create_violations(self.VIO2, self.LAW2)
        data = {
            "img": self.IMG_URL,
            "detected_time": self.DETECTED_TIME,
        }
        v_info2 = ViolationInfo.objects.create(**data)
        v_info2.violations.add(v1)
        v_info2.violations.add(v2)

        return v_info2

    def test_objs_create(self):
        cctv = self.create_cctv()
        v_info1 = self.create_violation_info_1()
        v_info2 = self.create_violation_info_2()
        print(cctv)
        print(v_info1)
        print(v_info2)
