# Service_Sell

```bash
APISERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
TOKEN=$(kubectl get secret $(kubectl get serviceaccount default -o jsonpath='{.secrets[0].name}') -o jsonpath='{.data.token}' | base64 --decode)
```

```yaml
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: all-reader
rules:
- apiGroups: [""] # "" indicates the core API group
  resources: ["services", "pods", "ingress", "deployments", "persistentvolumeclaims"]
  verbs: ["get", "watch", "list"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: all-reader-pod
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: all-reader
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
```
