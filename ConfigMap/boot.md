```bash
kubectl get configmap
```
 # create configmap from db.properties file
```bash
kubectl create configmap config-file --from-file=../db.properties
```
```bash
kubectl get configmap
```
# show ffile
```bash
kubectl get configmap config-map -o yml
```
# deete
```bash
kubectl delete cm config-map 
```
# create cm on commande
```bash
kubectl create cm newconfig --from-literal=env=test --from-literal=ipaddress=172.0.0.5
```
# show all commands of cm
```bash
kubectl create cm --help
```
