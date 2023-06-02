"""
Lifeguard integration with Kubernetes
"""


class LifeguardK8SPlugin:
    def __init__(self, lifeguard_context):
        self.lifeguard_context = lifeguard_context


def init(lifeguard_context):
    LifeguardK8SPlugin(lifeguard_context)
