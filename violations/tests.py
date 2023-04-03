from collections import defaultdict
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from cctvs.models import CCTV
from .models import Violation, ViolationInfo


class AllViolationsTest(APITestCase):
    """
    AllViolations view 테스트

    Endpoint:
        GET /api/violations/service/detail

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
            detected_time=datetime.now(),
        )
        self.violation_info1.violations.set(self.violations[:2])
        self.violation_info2 = ViolationInfo.objects.create(
            cctv=self.cctv,
            detected_time=datetime.now(),
        )
        self.violation_info2.violations.set(self.violations[1:])

    def test_all_violations(self):
        """
        Test the response of the AllViolations view.
        """
        url = reverse("all_violations")
        response = self.client.get(url)
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
