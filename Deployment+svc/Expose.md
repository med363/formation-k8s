# create clusterIP (access inside cluster between pods)
```bash
kubectl expose deployment apache-deployment --name=apache-svc --type=clusterIP --port=8080 --target-port=8080
```
# to access ocally to this svc I will forward pord of svc  
```bash
kubectl port-forward service/apache-svc
```
or directly on minikube
```bash
minikube service apache-svc
```
# expose svc to have some name of deployment
```bash
kubectl expose deployment nginx-deployment
```
