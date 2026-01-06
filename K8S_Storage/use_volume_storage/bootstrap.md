## first execcute redis
```bash
kubectl apply -f redis.yml
```
```bash
kubectl get po --watch
```
# other terminal
```bash
kubectl exec -it redis -- /bin/bash
```
```bash
ls
```
```bash
cd /data/redis
```
```bash
echo hello > file
```
```bash
cat file
```
```bash
apt update
```
```bash
apt install props (task manager)
```
```bash
ps aux
```
```bash
kill redis
```
**************** exple 2
```bash
kubectl apply -f ..yml
```
```bash
kubectl desc pod 
```
```bash
kubect exec -t .. -c ubuntu1 -- touch /ubuntu1/news
```
```bash
kubectl exec -it .. -c ubbuntu -- ls /ubuntu1
```
```bash
kubect exec -t .. -c ubuntu1 -- touch /ubuntu1/amine
```
```bash
kubectl exec -it .. -c ubbuntu1 -- ls /ubuntu1
```
```bash
kubectl exec -it .. -c ubbuntu2 -- ls /ubuntu2
```