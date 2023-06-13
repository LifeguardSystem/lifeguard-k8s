# Lifeguard K8S

Integration with Kubernetes

## Actions

- __delete_informed_pods__: delete pods informed in validation response details. Example of usage:

```python
from lifeguard_k8s.actions.pods import deleted_formed_pods

@validation(
    "drubin-lifeguard",
    actions=[delete_informed_pods],
    schedule={"every": {"minutes": 1}},
)
def drubin_lifeguard():
    # To execute delete_informed_pods action the response should have the
    # two attributes in details:
    # - namespace: the Kubernetes namespace where the pods are
    # - delete_pods: list of pods to be deleted
    return ValidationResponse(
        PROBLEM, {"delete_pods": ["lifeguard-75c44897b4-k9g94"], "namespace": "drubin"}
    )
```

## Validations

- __pods_validation__: check if all pods are running

**Important**:
To use Kubernetes APIs into the valiations, you need to create a service account and a cluster role binding. Example of a valid manifest:

```yaml
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: lifeguard-sa
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: lifeguard-roles
rules:
  - apiGroups: [""]
    resources: ["nodes"]
    verbs: ["get", "list"]
  - apiGroups: [""]
    resources: ["pods", "pods/exec"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: lifeguard-rolebinding
subjects:
  - kind: ServiceAccount
    name: lifeguard-sa
    namespace: namespace
roleRef:
  kind: ClusterRole
  name: lifeguard-roles
  apiGroup: rbac.authorization.k8s.io
```

