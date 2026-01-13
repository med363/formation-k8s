```bash
kubectl create secret generic test-secret --from-literal='username=admin' --from-literal='password=987654we$'
```
## show commands
```bash
kubectl create secret generic -h
```
## create secret for db
```bash
kubectl create secret generic my-secret --from-literal=MARIADB_ROOT_PASSWORD=passcode1
```
# show pwd
```bash
kubectl get secret
```
# show desc of my-secret
```bash
kubectl describe secret my-secret 
```
# show my secret file
```bash
kubectl get secret my-secret -o yaml
```
# assign secret to pod
```bash
kubectl run mariadb-test-pod --image=mariadb --env="MARIADB_ROOT_PASSWORD=secret"
```
# show pod
```bash
kubectl get pod
```
## create dep
```bash
kubectl create deployment mariadb --image=mariadb
```
# it does not work because not assign any key
```bash
kubectl get pod
```
```bash
kubectl set env deploy mariadb --from=secret/my-secret
```
# show all variable of pod 
```bash
kubectl exec .. -- env
```