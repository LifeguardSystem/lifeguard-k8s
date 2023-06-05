# Lifeguard K8S

Integration with Kubernetes

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

