from lifeguard import NORMAL, PROBLEM, change_status
from lifeguard.validations import ValidationResponse

from lifeguard_k8s.infrastructure.pods import get_not_running_pods

IN_REVIEW = {}


def pods_validation(namespace):
    status = NORMAL

    details = {"pods": []}

    if namespace not in IN_REVIEW:
        IN_REVIEW[namespace] = []

    if pods := get_not_running_pods(namespace):
        for pod in pods:

            if pod in IN_REVIEW[namespace]:

                status = change_status(status, PROBLEM)
                details["pods"] = pods
            else:
                IN_REVIEW[namespace].append(pod)

    for pod in IN_REVIEW[namespace]:
        if pod not in pods:
            IN_REVIEW[namespace].remove(pod)

    return ValidationResponse(status, details)
