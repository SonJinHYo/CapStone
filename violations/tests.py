from collections import defaultdict
from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from cctvs.models import CCTV
from .models import Violation, ViolationInfo


class AllViolationsTest(APITestCase):
    """
    AllViolations view 테스트

    Endpoint:
        GET self.base_url+/service/detail

    Request Parameters:
        None


    """

    def setUp(self):
        self.cctv = CCTV.objects.create(name="Test CCTV", region="Test Region")
        self.violations = [
            Violation.objects.create(name=name)
            for name in ["violation1", "violation2", "violation3"]
        ]
        self.violation_info1 = ViolationInfo.objects.create(
            cctv=self.cctv,
            detected_time=timezone.now(),
        )
        self.violation_info1.violations.set(self.violations[:2])
        self.violation_info2 = ViolationInfo.objects.create(
            cctv=self.cctv,
            detected_time=timezone.now(),
        )
        self.violation_info2.violations.set(self.violations[1:])

    def test_all_violations(self):
        """
        Test the response of the AllViolations view.
        """
        url = reverse("all_violations")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check instance type
        data = response.data
        self.assertIsInstance(data, dict)

        # check violation count
        expected_violation_cnt = defaultdict(int)
        for violation_info in ViolationInfo.objects.all():
            for violation in violation_info.__str__().split(","):
                expected_violation_cnt[violation] += 1
        self.assertDictEqual(expected_violation_cnt, data["violationCountObj"])

        # check region count
        expected_region_cnt = defaultdict(int)
        for violation_info in ViolationInfo.objects.all():
            expected_region_cnt[violation_info.cctv.region] += 1
        self.assertDictEqual(expected_region_cnt, data["regionCountObj"])

        # check detected hour count
        expected_detected_hour_cnt = defaultdict(int)
        for violation_info in ViolationInfo.objects.all():
            expected_detected_hour_cnt[violation_info.detected_time.hour] += 1
        self.assertDictEqual(expected_detected_hour_cnt, data["detectedHourCountObj"])


class ViolationDetailTestCase(APITestCase):
    def setUp(self):
        self.cctv1 = CCTV.objects.create(name="Test CCTV1", region="Test Region1")
        self.cctv2 = CCTV.objects.create(name="Test CCTV2", region="Test Region2")
        self.violations = [
            Violation.objects.create(name=name)
            for name in ["violation1", "violation2", "violation3"]
        ]
        self.violation_info1 = ViolationInfo.objects.create(
            cctv=self.cctv1,
            detected_time=timezone.now(),
        )
        self.violation_info1.violations.set(self.violations[:2])
        self.violation_info2 = ViolationInfo.objects.create(
            cctv=self.cctv2,
            detected_time=timezone.now(),
        )
        self.violation_info2.violations.set(self.violations[1:])
        self.base_url = "/api/v1/violations/service/"

    def test_violations_service_violation(self):
        # Test GET request with choice1 as "violation"
        def violation_url(N):
            """입력받은 숫자의 violationN url 반환"""
            return reverse("violation_detail", args=["violation", "violation" + str(N)])

        response = self.client.get(violation_url(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(violation_url(2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(violation_url(3))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(violation_url(4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_violations_service_region(self):
        # Test GET request with choice1 as "region"

        def region_url(N):
            """입력받은 숫자의 violationN url 반환"""
            return reverse("violation_detail", args=["region", "Test Region" + str(N)])

        response = self.client.get(region_url(1))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.client.get(region_url(2))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_violations_service_time(self):
        # Test GET request with choice1 as "time"
        def time_url(date_time):
            """입력받은 숫자의 violationN url 반환"""
            return reverse("violation_detail", args=["time", date_time])

        response = self.client.get(time_url("2023_04_04"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(time_url("2023_04_03"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.get(time_url("2023_04_05"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        # invalid time test
        self.assertEqual(
            self.client.get(time_url("2023_01")).status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            self.client.get(time_url("2023_02_")).status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            self.client.get(time_url("2023_03_33")).status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            self.client.get(time_url("2023_string_33")).status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_violations_service_invalid(self):
        # Test GET request with invalid choice1
        response = self.client.get(
            reverse("violation_detail", args=["invalid", "invalid"])
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# class ChoiceTestCase(APITestCase):
#     def test_get_violation(self):
#         url = reverse("choice", args=["violation"])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # 모든 위반 정보 객체의 이름이 응답값에 존재하는지 확인합니다.
#         violations = Violation.objects.all()
#         for violation in violations:
#             self.assertIn(violation.name, response.data)

#     def test_get_region(self):
#         url = reverse("choice", args=["region"])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # 모든 CCTV 객체의 지역 정보가 응답값에 존재하는지 확인합니다.
#         cctvs = CCTV.objects.all()
#         for cctv in cctvs:
#             self.assertIn(cctv.region, response.data)

#     def test_get_time(self):
#         url = reverse("choice", args=["time"])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_invalid_kind(self):
#         url = reverse("choice", args=["invalid_kind"])
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
