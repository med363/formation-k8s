### Prerequisites
2 or 3 Ubuntu 20.04 LTS System with Minimal Installation
Minimum 2 or more CPU, 3 GB RAM.
Disable SWAP on All node
SSH Access with sudo privileges



Server 1= master
Server 2= node1
Server 3= node2

```bash
sudo hostnamectl set-hostname "master"
```
```bash
sudo hostnamectl set-hostname "node1"
```
```bash
sudo hostnamectl set-hostname "node2"
```

#### Disable swap

```bash
swapoff -a
```
```bash
 sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab
```


Also comment out the reference to swap in /etc/fstab. Start by editing the below file:
```bash
sudo nano /etc/fstab
```

- Reboot the system to take effect

```bash
sudo reboot
```
- Update the system Packages

```bash
sudo apt-get update
```

### 1. Run these commands on Master/worker nodes

- install below packages if not installed

```bash
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```
- Add the Docker official GPG Key

```bash
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```
- Add the Docker APT repository


```bash
echo   "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu   $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- Update the System Packages

```bash
sudo apt-get update -y
```
- Install docker community edition and container runtime on both master and worker node

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io -y
```
- Add the Docker Daemon configurations to use systemd as the cgroup driver.

```bash
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF
```


- Add the docker user in group and give permission for docker.sock

```bash
sudo usermod -aG docker $USER
```
- Start the Docker service if not started

```bash
sudo systemctl start docker.service
```
- To check the docker service status

```bash
sudo systemctl status docker.service
```
- Enable Docker service at startup

```bash
sudo systemctl enable docker.service
```
- Restart the Docker service

```bash
sudo systemctl restart docker
```
### 2. Add Kubernetes GPG Key on All node
- Add Kubernetes GPG key in all node.
```bash
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
```

### 3. Add Kubernetes APT Repository on All node
- Add Kubernetes apt repository on all node for Ubuntu.

```bash
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

- update the system packages
```bash
sudo apt-get update
```

### 4. Install Kubeadm,Kubelet and Kubectl on All Node
- Install kubeadm,kubelet and kubectl using below command.

```bash
sudo apt-get install -y kubelet kubeadm kubectl
```
- Hold the packages to being upgrade

```bash
sudo apt-mark hold kubelet kubeadm kubectl
```

### 5. Initialize the Master node using kubeadm (on Master Node)
- Next initialize the master node using kubeadm.

```bash
sudo kubeadm init --pod-network-cidr 10.0.0.0/16
```

Output:
```bash
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 172.31.6.177:6443 --token vr5rat.seyprj6jvw4xy43m \
        --discovery-token-ca-cert-hash sha256:4c9b53eb03744b4cf21c5bdacd712024eb09030561714cc5545838482c8017b3
As above output mentioned copy the token in your notepad, we will need to join worker/slave to master node
```

Create new ‘.kube’ configuration directory and copy the configuration ‘admin.conf’ from ‘/etc/kubernetes’ directory.

```bash
sudo mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
To check kubeadm version.

```bash
kubeadm version
```
To check master node status

```bash
kubectl get nodes
```
### 6. Configure Pod Network and Verify Pod namespaces (on Master Node)
- Install the Weave network plugin to communicate master and worker nodes.

```bash
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml 
```
Output:

```bash
serviceaccount/weave-net created

clusterrole.rbac.authorization.k8s.io/weave-net created

clusterrolebinding.rbac.authorization.k8s.io/weave-net created

role.rbac.authorization.k8s.io/weave-net created

rolebinding.rbac.authorization.k8s.io/weave-net created

daemonset.apps/weave-net created
```

Check node status
```bash
kubectl get nodes
```
### 7. Join Worker Node to the Cluster (on all worker Node)
Next Join two worker nodes to master (adopt this command to your environment) .

```bash
sudo kubeadm join 172.31.6.177:6443 --token vr5rat.seyprj6jvw4xy43m --discovery-token-ca-cert-hash sha256:4c9b53eb03744b4cf21c5bdacd712024eb09030561714cc5545838482c8017b3
```
Output:

```bash
This node has joined the cluster:
* Certificate signing request was sent to apiserver and a response was received.
* The Kubelet was informed of the new secure connection details.

Run 'kubectl get nodes' on the control-plane to see this node join the cluster.
```

In case you forgot to copy the join command 

```bash
kubeadm token create --print-join-command
```

Check the All node status

```bash
sudo kubectl get nodes
```
Output:

```bash
Status:

NAME               STATUS   ROLES    AGE     VERSION

ip-172-31-16-180   Ready    master   3m19s   v1.20.5

ip-172-31-16-86    Ready    worker1   6m15s   v1.20.5

ip-172-31-21-34    Ready    worker2   3m23s   v1.20.5
```
To Verify Pod namespaces

```bash
kubectl get pods --all-namespaces
```
### exple of deployement server web
### Create pod without Manifestfile
```bash
kubectl run nginx --image nginx
```
### Show inf about pod
```bash
kubectl describe po nginx
```
### delete pod 
```bash
kubectl delete po nginx
```

### 1.Create Pod ==> Pod contain 1-n containers
### Manifest files ==>  my-pod.yml
```bash
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
  labels:
    type: webserver
spec:
  containers:
  - name: nginx-container
    image: nginx:latest
```
### Apply this file my-pod.yml
```bash
kubectl apply -f my-pod.yml
```
### Show Pod
```bash
kubectl get po
```

### 2.Creat replicaset object rs.yml
```bash 
#4 elts principale apiVersion ,kind(pod [[restart auto ]], Replicaset[[si node down replicat auto sur une autre node]],Deploiment[[]]),metadata[[dictionaire ]],spec[[specification:template of containers]]
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: my-replicatset
  labels:
    type: rs
spec:
  replicas: 7
  template:
    metadata:
      name: my-pod
      labels:
        type: webserver
    spec:
        containers:
        - name: nginx-container
          image: nginx:latest
#gere les objet nouvellement cree 
  selector:
    matchLabels:
      type: webserver 
```
### Apply file
```bash
kubectl apply -f rs.yml
```
### Master node echo for 5 min hertbit of other node 
### add replicat without Manifestfile
```bash
kubectl scale --replicas=22 -f <file of replicaset>
```
### scale down
```bash
kubectl scale --replicas=4 -f <file of replicaset> 
```
### delete replicaset to do deployement objet
```bash
kubectl delete replicaset my-replicatset
```

### defference between deployement and replicat that with deployement can do update and rollback
### 3.Create Deployment object
```bash
#4 elts principale apiVersion ,kind(pod [[restart auto ]], Replicaset[[si node down replicat auto sur une autre node]],Deploiment[[]]),metadata[[dictionaire ]],spec[[specification:template of containers]]
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
  labels:
    type: rs
spec:
  replicas: 7
  template:
    metadata:
      name: my-pod
      labels:
        type: webserver
    spec:
        containers:
        - name: nginx-container
          image: nginx:latest
#gere les objet nouvellement cree 
  selector:
    matchLabels:
      type: webserver 
```
### Apply this file deploy.yml
```bash
kubectl apply -f deploy.yml
```
### show all pod and wich node created
```bash
kubectl get po -o wide
```
### or
```bash
kubectl get po -o wide --show-labels
```

### 6.create service that pod be accesible outside there are three svcs (clusteIP,loadbalancer,NodePort)
### create nodeport svc nodeport.yml
```bash 
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  ports:
#port of container inside pod
  - targetPort: 80
#port de service prend flux 3000 redirection vers port du pod
    port: 80
#port phy 3ibaratan map 3000 redirger vers port du service 80
    nodePort: 30000
#ya3ref les pods ili na7ki a3lihom ->label pod
  selector:
    type: webserver
```
### Apply svc
```bash
kubectl apply -f nodeport.yml
```
### show svc
```bash
kubectl get svc
```
### show all
```bash
kubectl get all
```

### show containers run on backend
```bash
kubectl get daemonsets -n kube-system
```
### show health of cluster k8s
```bash
kubectl get componentstatuses
```

### -------------------------------------------------------rolling update ---------------------------------------------------------------------
### upgrade nginx to 1.17
### manifest file 
```bash
#4 elts principale apiVersion ,kind(pod [[restart auto ]], Replicaset[[si node down replicat auto sur une autre node]],Deploiment[[]]),metadata[[dictionaire ]],spec[[specification:template of containers]]
# hw does know how to should manage pods and replicaset->labels
apiVersion: apps/v1
kind: Deployment
metadata:
  
#manage pod on enviroment test
  labels:
    environment: testdeploy
  name: testdeploy
spec:
  replicas: 3
#gere les objet nouvellement cree 
  selector:
#this label manage replicatset
    matchLabels:
      environment: test 
#how i upgrade my pod 1.16->1.17 if 1.17 tymchy labes mb3ad 10s nifsa5 one f old pod 1.16 then another pd will came with 1.17
  minReadySeconds: 10
  strategy: 
    rollingUpdate:
#new 1 pd with version 1.17((4 copy of the pod one of them 1.17))
     maxSurge: 1
# honi n9oli lazem hata pod ty5dim il kol lazem ye5dmo 3-0 =3 idha khalit maxUnivalable=1 => pod mata5dimch may9ala9ch 3-1=2
     maxUnavailable: 0
    type: RollingUpdate
  template:
    metadata:
#manage pod on enviroment test
      labels:
        environment: test
    spec:
        containers:
        - image: nginx:1.17
          name: nginx
```

### nodeport service
```bash
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  ports:
#port of container inside pod
  - targetPort: 80
#port de service prend flux 3000 redirection vers port du pod
    port: 80
#port phy 3ibaratan map 3000 redirger vers port du service 80
    nodePort: 3000
#ya3ref les pods ili na7ki a3lihom ->label pod
  selector:
    environment: test
```
