# show ns
```bash
kubectl get ns
```
# enter on ns ingress
```bash
kubectl get all -n ingress-nginx
```
# create nginx within svc
```bash
kubectl create deploy nginxservice --image=nginx:latest
```
```bash
kubectl scale deploy nginxservice --replicas=4
```
# show up 
```bash
kubectl get all
```
# create svc
```bash
kubectl expose deploy nginxservice --port=80 --type=NodePort
```
```bash
kubectl get svc
```
# create ingress
```bash
kubectl create ingress nginxsvc-ingress --rule="/=nginxservice:80"
```
```bash
kubectl get ingress
```
# show ip 
```bash
minikube ip
```
# connect ssh
```bash
minikube ssh
```
# create dns
```bash
sudo /bin/sh -c 'echo "192.168.X.X nginxsvc.io' >> /etc/hosts
```
```bash
cat /etc/hosts
```
```bash
curl nginxsvc.io
```
# show ing file
```bash
exit
```
```bash
kubectl edit ingress nginxsvc-ingress
```
#####
```bash
kubectl create deploy app1 --image=httpd:latest
```
```bash
kubectl create deploy app2 --image=gcr.io/google-samples/hello-app:1.0
```
```bash
kubectl create deploy app3 --image=gcr.io/google-samples/hello-app:2.0
```
```bash
kubectl scale deploy app1 --replicas=6
```
```bash
kubectl scale deploy app2 --replicas=4
```
```bash
kubectl scale deploy app3 --replicas=4
```
# show deployment
```bash
kubectl get deploy
```
# show all
```bash 
kubectl get all
```
# create svc 
```bash
kubectl expose deploy app1 --port=80 --type=NodePort
```
```bash
kubectl expose deploy app2 --port=8080 --type=NodePort
```
```bash
kubectl expose deploy app3 --port=8080 --type=NodePort
```
# show svc
```bash
kubectl get svc
```
# show svc on browser
```bash
minikube service app1
```
```bash
minikube service app2
```
```bash
minikube service app3
```
# fanout ing
```bash
k apply -f fanout.yml
```
# innf of ing
```bash
k describe ingress multiapp-ingress
```
# create dns in minikube 
```bash
minikube ssh
```
```bash
sudo /bin/sh -c 'echo "ip@ofminikube codographia.io" >> /etc/hosts
```
# test
```bash
curl codographia.io
```
```bash
curl codographia.io/app2
```
```bash
curl codographia.io/app3
```
#### named-based virtual hosting ingress 
```bash
kubectl create deploy ahly --image=nginx
```
```bash
kubectl create deploy zamalek --image=httpd
```
```bash
kubectl expose deploy ahly --port=80
```
```bash
kubectl expose deploy zamalek --port=80
```
# show 
```bash
kubectl get all
```
# create dns
```bash
minikube ssh
```
```bash
sudo /bin/sh -c 'echo "@ipminikube ahly.k8s" >> /etc/hosts'
```
```bash
sudo /bin/sh -c 'echo "@ipminikube zamalek.k8s" >> /etc/hosts'
```
```bash
cat /etc/hosts
```
# create ing virt host 
```bash
kubectl create ingress dawrymasry --rule="ahly.k8s/=ahly=80" --rule="zamalek.k8s/=zamalek:80"
```
# show ing that created
```bash
kubectl get ingress
```
```bash
minikube ssh
```
```bash
curl ahly.k8s
```
```bash
curl zamalek.k8s
```



