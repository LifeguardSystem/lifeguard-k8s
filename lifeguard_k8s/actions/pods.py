from lifeguard.logger import lifeguard_logger as logger

from lifeguard_k8s.infrastructure.pods import delete_a_pod


def delete_informed_pods(validation_response, _settings):
    """
    Action to delete informed pods

    :param validation_name: validation name
    :type validation_name: ValidationResponse
    :param _settings: settings
    :type _settings: dict

    :return: None
    """
    pods = validation_response.details.get("delete_pods", [])
    namespace = validation_response.details.get("namespace", "")

    for pod in pods:
        delete_a_pod(namespace, pod)
        logger.info("pod {} deleted".format(pod))
