from unittest.mock import MagicMock


def build_pod(status, container_status, pod_name, kind="ReplicaSet"):
    container_statuses = MagicMock(name="container_statuses")
    container_statuses.ready = container_status
    container_statuses.restart_count = 0
    container_statuses.name = "container_name"

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


def build_deployment(name, replicas, ready_replicas):
    deployment = MagicMock(name="deployment")
    deployment.metadata.name = name
    deployment.status.replicas = replicas
    deployment.status.ready_replicas = ready_replicas
    deployment.status.unavailable_replicas = 0
    return deployment
