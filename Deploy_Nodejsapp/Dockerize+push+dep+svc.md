## Dockerize
```bash
docker build . -t node
```
# push
```bash
docker login 
```
```bash
docker tag node mohamedamineblibech/node
```
```bash
docker push mohamedamineblibech/node
```
# Deployment
```bash
kubectl create deployment k8s-node --image=mohamedamineblibech/node
```
# svc clusterIP
```bash
kubectl expose deployment k8s-node --port=3000
```
# scale
```bash
kubectl scale deployment k8s-node --replicaset=6
```
# show ip of pods
```bash
kubectl get pods -o wide
```
# enter inside pod within minikube
```bash
minikube ssh
```
```bash
curl @pod:3000
```
## delete svc
```bash
kubectl delete svc k8s-node
```
## svc nodeport
```bash
kubectl expose deployment k8s-node --type=NodePort --port=3000
```
## show svc
```bash
kubectl get svc
```




