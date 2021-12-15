## Upgrade K8S Cluster

***keep in mind we update ONE minor version at a time!*** 


### 1. On the Master node
- Check the available version of kubeadm
```bash
apt-cache madison kubeadm
```
- Install the desired version
```bash
apt-get upgrade -y kubeadm=1.23.0-00
```
- execute the plan
```bash
kubeadm upgrade plan
```
- update the kubelet and restart it
```bash
sudo apt-get upgrade -y kubelet=1.23.0-00
sudo systemctl restart kubelet
```
- check that the version is updated
```bash
kubectl get nodes
```

### 2. On the worker nodes

- drain the node 
```bash
kubectl drain node1
```

- update the kubeadm version
```bash
sudo apt-get upgrade -y kubeadm=1.23.0-00
```
- update the kubelet and restart it
```bash
sudo apt-get upgrade -y kubelet=1.23.0-00
sudo systemctl restart kubelet
```
- upgrade the node 
```bash
sudo kubeadm upgrade node config --kubelet-version v1.23.0
```
- Uncordon the node 
```bash
kubectl uncordon node1
```
