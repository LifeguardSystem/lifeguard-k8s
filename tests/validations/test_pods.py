from unittest import TestCase
from unittest.mock import patch

from lifeguard import NORMAL, PROBLEM

from lifeguard_k8s.validations.pods import pods_validation


class ValidationsPodsTest(TestCase):
    @patch("lifeguard_k8s.validations.pods.get_not_running_pods")
    def test_normal_response(self, mock_get_not_running_pods):
        mock_get_not_running_pods.return_value = []

        response = pods_validation("namespace")

        mock_get_not_running_pods.assert_called_with("namespace")
        self.assertEqual(response.status, NORMAL)
        self.assertEqual(response.details, {"pods": []})
        self.assertEqual(response.settings, None)

    @patch("lifeguard_k8s.validations.pods.get_not_running_pods")
    def test_normal_response_on_first_error(self, mock_get_not_running_pods):
        mock_get_not_running_pods.return_value = ["pod"]

        response = pods_validation("namespace")

        self.assertEqual(response.status, NORMAL)
        self.assertEqual(response.details, {"pods": []})
        self.assertEqual(response.settings, None)

    @patch("lifeguard_k8s.validations.pods.IN_REVIEW", {"namespace": ["pod"]})
    @patch("lifeguard_k8s.validations.pods.get_not_running_pods")
    def test_error_response_on_second_error(self, mock_get_not_running_pods):
        mock_get_not_running_pods.return_value = ["pod"]

        response = pods_validation("namespace")

        self.assertEqual(response.status, PROBLEM)
        self.assertEqual(response.details, {"pods": ["pod"]})
        self.assertEqual(response.settings, None)

    @patch("lifeguard_k8s.validations.pods.IN_REVIEW", {"namespace": ["pod"]})
    @patch("lifeguard_k8s.validations.pods.get_not_running_pods")
    def test_normal_on_first_error_after_normalized(self, mock_get_not_running_pods):
        mock_get_not_running_pods.return_value = []

        response = pods_validation("namespace")

        mock_get_not_running_pods.return_value = ["pod"]

        response = pods_validation("namespace")

        self.assertEqual(response.status, NORMAL)
