from lifeguard_k8s.infrastructure import get_apps_client


def scale_a_deployment(namespace, deployment_name, replicas):
    apps_v1 = get_apps_client()
    apps_v1.patch_namespaced_deployment_scale(
        deployment_name, namespace, {"spec": {"replicas": replicas}}
    )
