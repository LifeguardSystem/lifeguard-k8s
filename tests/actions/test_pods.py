from unittest import TestCase
from unittest.mock import patch, call

from lifeguard.validations import ValidationResponse
from lifeguard_k8s.actions.pods import delete_informed_pods


class TestPods(TestCase):
    @patch("lifeguard_k8s.actions.pods.delete_a_pod")
    def test_delete_informed_pods(self, mock_delete_a_pod):
        validation_response = ValidationResponse(
            "NORMAL", {"delete_pods": ["pod1", "pod2"], "namespace": "namespace"}
        )
        delete_informed_pods(validation_response, {})
        mock_delete_a_pod.assert_has_calls(
            [call("namespace", "pod1"), call("namespace", "pod2")]
        )
