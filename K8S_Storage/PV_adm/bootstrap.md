```bash
kubectl apply -f pv.yml
```
```bash
kubectl get pv
```
```bash
kubectl describe pv pv-volume
```
########### pvc ###
# pvc is a request for a stge by a user.as pods consume node ressource and PVC consume PV resources.
```bash
kubectl create -f pvc.yml
```
# he have create auto volume (pv) related pvc bound that will be delete auto (retain policy Delete)
```bash
kubectl get pv
```
# show feature on minikube
```bash
minikube addons list
```



