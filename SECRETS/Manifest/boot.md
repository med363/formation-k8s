```bash
kubectl apply -f db-secret.yml
```
```bash 
kubectl get secret -o yml
```
##############
```bash
kubectl apply -f db-secret-un.yml
```
# create generic secret
```bash
kubectl create secret generic server-user --from-literal=server-username='ca_admin'
```
```bash
kubectl apply -f server-user.yaml
```
```bash
kubectl exec ... -- env
```
```bash
kubectl exec -it .. -- /bin/sh -c 'echo $SERVER_USER'
```
```bash
kubectl apply -f basic-auth.yml
```
```bash
kubectl get secret
```
```bash
kubectl apply -f my-secret.yml
```
```bash
kubectl apply -f pod-volume-secret.yml
```
# show volume in pod
```bash
kubectl exec -it secret-vol-pod -- /bin/bash
```
# then 
```bash
ls /etc/secret-volume
```
# show value of decode
```bash
echo "$( cat /etc/secret-volume/username )"
```
