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


def get_not_running_pods(namespace):
    not_running_pods = []

    if LIFEGUARD_KUBERNETES_CONFIG:
        config.load_kube_config(LIFEGUARD_KUBERNETES_CONFIG)
    else:
        config.load_incluster_config()

    v1 = client.CoreV1Api()
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
