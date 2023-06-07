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
        "LIFEGUARD_KUBERNETES_READ_LOG_MAX_SIZE": {
            "default": "500",
            "type": "int",
            "description": "max size of log to be read",
        },
    }
)

LIFEGUARD_KUBERNETES_CONFIG = SETTINGS_MANAGER.read_value("LIFEGUARD_KUBERNETES_CONFIG")
LIFEGUARD_KUBERNETES_READ_LOG_MAX_SIZE = SETTINGS_MANAGER.read_value(
    "LIFEGUARD_KUBERNETES_READ_LOG_MAX_SIZE"
)
