```bash
kubectl create -f pod-volume.yml
```
# we have create auto pv
```bash
kubectl get pv
```
# create folder
```bash
kubectl exec pod-nginx -- touch /usr/share/nginx/html/codographia
```
# show volume of provissioner that create pv 
```bash
minikube ssh
```
```bash
ls -l /tmp/hostpath-provisioner/default/my-pvc
```
