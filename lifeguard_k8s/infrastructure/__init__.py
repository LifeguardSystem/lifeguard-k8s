from kubernetes import client, config
from lifeguard_k8s.settings import (
    LIFEGUARD_KUBERNETES_CONFIG,
)


def _load_config():
    if LIFEGUARD_KUBERNETES_CONFIG:
        config.load_kube_config(LIFEGUARD_KUBERNETES_CONFIG)
    else:
        config.load_incluster_config()


def get_client():
    _load_config()
    return client.CoreV1Api()


def get_apps_client():
    _load_config()
    return client.AppsV1Api()
