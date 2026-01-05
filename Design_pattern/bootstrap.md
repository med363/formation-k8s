# apply file
```bash
kubectl apply -f ..yml
```
# show pod
```bash
kubectl get po
```
# show msg in pod 
```bash
kubectl exec -it nginx-helper-pod -c nginx-container -- /bin/bash
```
```bash
curl localhost
```
# show containers in pod
```bash 
kubectl get pods nginx-helper-pod -o jsonpath='{.spec.containers}[*].name}'
```
# show containers iin dashboard
```bash
minikube dashboard --url
```