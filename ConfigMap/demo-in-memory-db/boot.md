```bash
kubectl apply -f redis-configmap.yml
```
```bash
kubectl apply -f redis-pod.yml
```
# enter on redis
```bash
kubectl exec -it redis -- redis-cli
```
```bash
config get maxmemory
```
```bash
config get maxmemory-policy
```
