from unittest import TestCase
from unittest.mock import patch

from tests.infrastructure import build_pod, build_deployment

from lifeguard_k8s.infrastructure.namespaces import get_namespace_infos


class InfrastructureNamespacesTests(TestCase):
    @patch("lifeguard_k8s.infrastructure.config")
    @patch("lifeguard_k8s.infrastructure.client")
    def test_get_namespace_infos(self, mock_client, _mock_config):
        pod = build_pod("Running", True, "pod_name")
        deployment = build_deployment("deployment_name", 1, 1)

        mock_client.CoreV1Api.return_value.list_namespaced_pod.return_value.items = [
            pod
        ]

        mock_client.AppsV1Api.return_value.list_namespaced_deployment.return_value.items = [
            deployment
        ]

        self.assertEqual(
            get_namespace_infos("namespace"),
            {
                "deployments": [
                    {
                        "name": "deployment_name",
                        "ready_replicas": 1,
                        "replicas": 1,
                        "unavailable_replicas": 0,
                    }
                ],
                "pods": [
                    {
                        "containers": [
                            {
                                "name": "container_name",
                                "ready": True,
                                "restart_count": 0,
                            }
                        ],
                        "name": "pod_name",
                        "status": "Running",
                    }
                ],
            },
        )
