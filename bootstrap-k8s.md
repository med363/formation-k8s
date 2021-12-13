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
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"
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

