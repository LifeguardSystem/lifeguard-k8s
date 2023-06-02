"""
Lifeguard K8S Settings
"""
from lifeguard.settings import SettingsManager

SETTINGS_MANAGER = SettingsManager(
    {
        "LIFEGUARD_KUBERNETES_CONFIG": {
            "default": "",
            "description": "path to kube config",
        },
    }
)

LIFEGUARD_KUBERNETES_CONFIG = SETTINGS_MANAGER.read_value("LIFEGUARD_KUBERNETES_CONFIG")
