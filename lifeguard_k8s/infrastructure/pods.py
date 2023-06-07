from kubernetes import client, config
from lifeguard_k8s.settings import LIFEGUARD_KUBERNETES_CONFIG

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


def _get_clients():
    if LIFEGUARD_KUBERNETES_CONFIG:
        config.load_kube_config(LIFEGUARD_KUBERNETES_CONFIG)
    else:
        config.load_incluster_config()

    return client.CoreV1Api()


def get_not_running_pods(namespace):
    not_running_pods = []

    v1 = _get_clients()
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


def get_events_from_pod(namespace, pod_name):
    v1 = _get_clients()
    events = v1.list_namespaced_event(
        namespace, field_selector=f"involvedObject.name={pod_name}"
    )

    return [{"event_type": item.type, "message": item.message} for item in events.items]


def get_last_error_event_from_pod(namespace, pod_name):
    events = get_events_from_pod(namespace, pod_name)
    events = [event for event in events if event["event_type"] != "Normal"]

    if events:
        return events[-1]

    return None
