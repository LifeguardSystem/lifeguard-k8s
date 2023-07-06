from lifeguard_k8s.infrastructure import get_client, get_apps_client


def get_namespace_infos(namespace):
    """
    Return current main infos of a namespace
    """
    infos = {"pods": [], "deployments": []}

    v1 = get_client()
    apps_v1 = get_apps_client()

    pods = v1.list_namespaced_pod(namespace)
    deployments = apps_v1.list_namespaced_deployment(namespace)

    for pod in pods.items:
        infos["pods"].append(
            {
                "name": pod.metadata.name,
                "status": pod.status.phase,
                "containers": [
                    {
                        "name": container.name,
                        "ready": container.ready,
                        "restart_count": container.restart_count,
                    }
                    for container in pod.status.container_statuses
                ],
            }
        )

    for deployment in deployments.items:
        infos["deployments"].append(
            {
                "name": deployment.metadata.name,
                "replicas": deployment.status.replicas,
                "ready_replicas": deployment.status.ready_replicas,
                "unavailable_replicas": deployment.status.unavailable_replicas,
            }
        )
    return infos
