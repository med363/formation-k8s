## Dockerize
```bash
docker build . -t node
```
# push
```bash
docker login 
```
```bash
docker tag node mohamedamineblibech/node:v2.0
```
```bash
docker push mohamedamineblibech/node:v2.0
```
# Deployment
```bash
kubectl set image deploy k8s-node k8s-node=mohamedamineblibech/node:v2.0
```
# show rolling
```bash
kubectl rollout status  deployment/k8s-node 
```
# show ip of pods
```bash
kubectl get pods -o wide
```
# test
```bash
minikube service k8s-node
```
# retun to my previous image
```bash
kubectl set image deploy k8s-node k8s-node=mohamedamineblibech/node
```
# show ip of pods
```bash
kubectl get pods -o wide
```