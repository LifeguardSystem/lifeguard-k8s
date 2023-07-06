from lifeguard_k8s.infrastructure import get_client
from lifeguard_k8s.settings import (
    LIFEGUARD_KUBERNETES_READ_LOG_MAX_SIZE,
)

RUNNING_STATUS = "Running"
COMPLETED_STATUS = "Succeeded"

NORMAL_STATUSES = [RUNNING_STATUS, COMPLETED_STATUS]


def _check_if_job_pod(pod):
    return pod.metadata.owner_references[0].kind == "Job"


def _exists_success_pod_after_job(job_pod, pods):
    for pod in pods.items:
        if (
            job_pod.metadata.owner_references[0].name in pod.metadata.name
            and pod.status.phase == COMPLETED_STATUS
        ):
            return True
    return False


def get_not_running_pods(namespace):
    not_running_pods = []

    v1 = get_client()
    pods = v1.list_namespaced_pod(namespace)

    for pod in pods.items:
        if pod.status.phase not in NORMAL_STATUSES or (
            not all(container.ready for container in pod.status.container_statuses)
        ):
            if _check_if_job_pod(pod):
                if not _exists_success_pod_after_job(pod, pods):
                    not_running_pods.append(pod.metadata.name)
            else:
                not_running_pods.append(pod.metadata.name)

    return not_running_pods


def delete_a_pod(namespace, pod_name):
    v1 = get_client()
    v1.delete_namespaced_pod(pod_name, namespace)


def get_events_from_pod(namespace, pod_name):
    v1 = get_client()
    events = v1.list_namespaced_event(
        namespace, field_selector=f"involvedObject.name={pod_name}"
    )
    return [
        {"event_type": item.type, "message": item.message, "reason": item.reason}
        for item in events.items
    ]


def get_last_error_event_from_pod(namespace, pod_name):
    events = get_events_from_pod(namespace, pod_name)
    events = [event for event in events if event["event_type"] != "Normal"]

    if events:
        failed = [event for event in events if event["reason"] == "Failed"]
        if failed:
            return failed[-1]
        return events[-1]

    return None


def get_logs_from_pod(namespace, pod_name):
    v1 = get_client()
    log = v1.read_namespaced_pod_log(pod_name, namespace)
    return log[-LIFEGUARD_KUBERNETES_READ_LOG_MAX_SIZE:]
