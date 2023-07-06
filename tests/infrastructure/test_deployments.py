from unittest import TestCase
from unittest.mock import patch

from lifeguard_k8s.infrastructure.deployments import scale_a_deployment


class InfrastructureDeploymentsTests(TestCase):
    @patch("lifeguard_k8s.infrastructure.config")
    @patch("lifeguard_k8s.infrastructure.client")
    def test_scale_a_deployment(self, mock_client, _mock_config):
        patch_namespaced_deployment_scale = (
            mock_client.AppsV1Api.return_value.patch_namespaced_deployment_scale
        )
        patch_namespaced_deployment_scale.return_value = ""

        scale_a_deployment("namespace", "deployment_name", 1)

        patch_namespaced_deployment_scale.assert_called_with(
            "deployment_name", "namespace", {"spec": {"replicas": 1}}
        )
