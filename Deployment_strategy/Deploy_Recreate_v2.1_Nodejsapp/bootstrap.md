# apply first deployment
```bash
kubectl apply -f deployment.yml
```
# check pod 
```bash
kubectl get all
```
# apply svc
```bash
kubectl apply -f service.yml
```
# show pod on browser
```bash
minikube service recreate-svc
```
# apply second deployment
```bash
kubectl apply -f deployment2.yml
```
# check recreate tpod 
```bash 
kubectl get po
```
# show pod on browser
```bash
minikube service recreate-svc
```
# return to first version 
```bash
kubectl apply -f deployment.yml
```
# show rollout
```bash
kubectl rollout status deployment/recreate-deployment
```
# show pod on browser
```bash
minikube service recreate-svc
```