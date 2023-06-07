from lifeguard import NORMAL, PROBLEM, change_status
from lifeguard.validations import ValidationResponse

from lifeguard_k8s.infrastructure.pods import (
    get_not_running_pods,
    get_last_error_event_from_pod,
)

IN_REVIEW = {}


def pods_validation(namespace):
    status = NORMAL

    details = {"pods": [], "traceback": []}

    if namespace not in IN_REVIEW:
        IN_REVIEW[namespace] = []

    pods = get_not_running_pods(namespace)
    if pods:
        for pod in pods:
            if pod in IN_REVIEW[namespace]:
                status = change_status(status, PROBLEM)
                details["pods"].append(pod)

                last_error = get_last_error_event_from_pod(namespace, pod)
                if last_error:
                    details["traceback"].append(last_error["message"])
                else:
                    details["traceback"].append(None)
            else:
                IN_REVIEW[namespace].append(pod)

    for pod in IN_REVIEW[namespace]:
        if pod not in pods:
            IN_REVIEW[namespace].remove(pod)

    return ValidationResponse(status, details)
