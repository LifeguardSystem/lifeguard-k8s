from unittest import TestCase
from unittest.mock import patch, MagicMock

from lifeguard_k8s.infrastructure.pods import (
    get_not_running_pods,
    get_events_from_pod,
    get_last_error_event_from_pod,
)


def build_pod(status, container_status, pod_name, kind="ReplicaSet"):
    container_statuses = MagicMock(name="container_statuses")
    container_statuses.ready = container_status

    owner_reference = MagicMock(name="owner_reference")
    owner_reference.kind = kind
    owner_reference.name = pod_name

    pod = MagicMock(name="pod")
    pod.status = MagicMock(name="status")
    pod.status.phase = status
    pod.status.container_statuses = [container_statuses]
    pod.metadata.name = pod_name
    pod.metadata.owner_references = [owner_reference]

    return pod


class InfrastructurePodsTests(TestCase):
    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_not_return_pod_if_has_normal_statuses(self, mock_client, mock_config):
        pod = build_pod("Running", True, "pod_name")

        mock_client.CoreV1Api.return_value.list_namespaced_pod.return_value.items = [
            pod
        ]

        self.assertEqual(get_not_running_pods("namespace"), [])
        mock_config.load_incluster_config.assert_called()

    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_return_pod_if_not_has_normal_statuses(self, mock_client, _mock_config):
        pod = build_pod("Failed", True, "pod_name")

        mock_client.CoreV1Api.return_value.list_namespaced_pod.return_value.items = [
            pod
        ]

        self.assertEqual(get_not_running_pods("namespace"), ["pod_name"])

    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_return_pod_if_not_has_all_containers_ready(
        self, mock_client, _mock_config
    ):
        pod = build_pod("Running", False, "pod_name")

        mock_client.CoreV1Api.return_value.list_namespaced_pod.return_value.items = [
            pod
        ]

        self.assertEqual(get_not_running_pods("namespace"), ["pod_name"])

    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_return_pod_if_is_job_and_not_has_success_pod_after_job(
        self, mock_client, _mock_config
    ):
        pod = build_pod("Failed", True, "pod_name", kind="Job")

        mock_client.CoreV1Api.return_value.list_namespaced_pod.return_value.items = [
            pod
        ]

        self.assertEqual(get_not_running_pods("namespace"), ["pod_name"])

    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_not_return_pod_if_is_job_and_has_success_pod_after_job(
        self, mock_client, _mock_config
    ):
        pod = build_pod("Failed", True, "pod_name", kind="Job")
        success_pod = build_pod("Succeeded", True, "pod_name", kind="Job")

        mock_client.CoreV1Api.return_value.list_namespaced_pod.return_value.items = [
            pod,
            success_pod,
        ]

        self.assertEqual(get_not_running_pods("namespace"), [])

    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_get_events_from_pod(self, mock_client, _mock_config):
        event = MagicMock(name="event")
        event.type = "Normal"
        event.message = "message"
        mock_client.CoreV1Api.return_value.list_namespaced_event.return_value.items = [
            event
        ]

        self.assertEqual(
            get_events_from_pod("namespace", "pod_name"),
            [{"event_type": "Normal", "message": "message"}],
        )

    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_get_last_error_event_from_pod_without_errors(
        self, mock_client, _mock_config
    ):
        event = MagicMock(name="event")
        event.type = "Normal"
        event.message = "message"
        mock_client.CoreV1Api.return_value.list_namespaced_event.return_value.items = [
            event
        ]

        self.assertEqual(
            get_last_error_event_from_pod("namespace", "pod_name"),
            None,
        )

    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_get_last_error_event_from_pod_with_errors(self, mock_client, _mock_config):
        event_normal = MagicMock(name="event")
        event_normal.type = "Normal"
        event_normal.message = "message"

        event_error = MagicMock(name="event")
        event_error.type = "Warning"
        event_error.message = "message"

        mock_client.CoreV1Api.return_value.list_namespaced_event.return_value.items = [
            event_error,
            event_normal,
        ]

        self.assertEqual(
            get_last_error_event_from_pod("namespace", "pod_name"),
            {"event_type": "Warning", "message": "message"},
        )

    @patch(
        "lifeguard_k8s.infrastructure.pods.LIFEGUARD_KUBERNETES_CONFIG",
        "path_to_file",
    )
    @patch("lifeguard_k8s.infrastructure.pods.config")
    @patch("lifeguard_k8s.infrastructure.pods.client")
    def test_call_load_kube_config_if_config_is_not_empty(
        self, mock_client, mock_config
    ):
        mock_client.CoreV1Api.return_value.list_namespaced_pod.return_value.items = []

        self.assertEqual(get_not_running_pods("namespace"), [])
        mock_config.load_kube_config.assert_called_with("path_to_file")
