## High-Level Example Workflow: 
# 1. A user deploys a Kubernetes manifest specifying desired pod configurations. 
# 2. The manifest is submitted to the API server. 
# 3. The API server stores the configuration in etcd. 
# 4. The Controller Manager detects the desired state and instructs the Kubelet on worker nodes to start or stop containers. 
# 5. Kubelet communicates with the container runtime to execute the desired state. 
# 6. Kube Proxy manages network rules, enabling communication between pods

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
# View nodes in the cluster
```bash
kubectl get nodes
``` 
# Describe a node 
```bash
kubectl describe node <node-name>
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
1. View Kubernetes cluster information:
```bash 
kubectl cluster-info
```
3. View nodes in the cluster:
```bash
kubectl get nodes
```
5. View all resources in a namespace:
```bash
kubectl get all -n <namespace>
```
7. Describe a specific resource:
```bash
kubectl describe <resource_type> <resource_name>
```
9. View pod logs:
```bash
kubectl logs <pod_name>
```
# View pods in the default namespace 
```bash
kubectl get pods
``` 
# Scale a deployment 
```bash
kubectl scale deployment <deployment-name> --replicas=3
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

## Deployments and Pods: 
6. Create a deployment:
```bash
kubectl create deployment <deployment_name> --image=<image_name>
```
8. Scale a deployment:
```bash
kubectl scale deployment <deployment_name> --replicas=<replica_count>
```
10. Rolling restart of a deployment:
```bash
kubectl rollout restart deployment <deployment_name>
```
12. Exposing a deployment as a service:
```bash
kubectl expose deployment <deployment_name> --port=<port>
```
14. Run a one-time command in a pod:
```bash
kubectl exec -it <pod_name> -- <command>
```
## Services: 
16. Create a service:
```bash
kubectl create service <service_type> <service_name> -
tcp=<port>:<target_port>
```
18. Expose a deployment using a service:
```bash 
kubectl expose deployment <deployment_name> --type=<service_type> -
port=<port>
``` 
20. Describe a service:
```bash
kubectl describe service <service_name>
```
22. Delete a service:
```bash
kubectl delete service <service_name>
````
## Configurations: 
24. View ConfigMap details:
```bash
kubectl get configmap <configmap_name>
```
26. Create a ConfigMap from file:
```bash
kubectl create configmap <configmap_name> --from-file=<path/to/files>
```
28. View Secret details:
```bash
kubectl get secret <secret_name>
```
30. Create a Secret from literal values: 
kubectl create secret generic <secret_name> --from-literal=key1=value1 -
from-literal=key2=value2 
Networking: 
31. Get information about services and their endpoints: 
kubectl get svc 
32. Create an Ingress resource: 
kubectl apply -f ingress.yaml 
33. View Ingress details: 
kubectl get ingress 
34. Network policy details: 
kubectl get networkpolicies 
35. Enable or disable resource access for a pod: 
kubectl apply -f network-policy.yaml 
Storage: 
36. View Persistent Volumes (PVs): 
kubectl get pv 
37. View Persistent Volume Claims (PVCs): 
kubectl get pvc 
38. Create a Persistent Volume Claim: 
kubectl apply -f persistent-volume-claim.yaml 
Scaling and Autoscaling: 
39. Autoscale a deployment: 
kubectl autoscale deployment <deployment_name> --min=<min_replicas> -
max=<max_replicas> --cpu-percent=<cpu_percent> 
40. View horizontal pod autoscaler details: 
kubectl get hpa 
41. Manually trigger horizontal pod autoscaler: 
kubectl scale deployment <deployment_name> --replicas=<new_replica_count> 
StatefulSets: 
42. Create a StatefulSet: 
kubectl apply -f statefulset.yaml 
43. Scale a StatefulSet: 
kubectl scale statefulset <statefulset_name> --replicas=<replica_count> 
44. Delete a StatefulSet and associated pods: 
kubectl delete statefulset <statefulset_name> 
Debugging and Troubleshooting: 
45. Run a debug container in a pod: 
kubectl debug <pod_name> -it --image=<debug_image> 
46. Get events in the cluster: 
kubectl get events 
47. Check pod resource usage: 
kubectl top pod 
Security: 
48. View pod security policies: 
kubectl get psp 
49. View pod security context: 
kubectl get pods --output=jsonpath='{range 
.items[*]}{"\n"}{.metadata.name}{":"}{.spec.securityContext.runAsUser}{end}
 ' 
50. Create a service account: 
kubectl create serviceaccount <serviceaccount_name> 
Namespaces: 
51. List all namespaces: 
kubectl get namespaces 
52. Switch to a different namespace: 
kubectl config set-context --current --namespace=<namespace_name> 
53. Create a namespace: 
kubectl create namespace <namespace_name> 
Helm (Kubernetes Package Manager): 
54. Install a Helm chart: 
helm install <release_name> <chart_name> 
55. List Helm releases: 
helm list 
56. Upgrade a Helm release: 
helm upgrade <release_name> <chart_name> 
Monitoring and Logging: 
57. View pod logs with timestamps: 
kubectl logs <pod_name> --timestamps 
58. Enable metrics server (for resource usage metrics): 
kubectl apply -f https://github.com/kubernetes-sigs/metrics
server/releases/latest/download/components.yaml 
59. View resource usage metrics for nodes: 
kubectl top nodes 
60. View resource usage metrics for pods: 
kubectl top pods 
Clean Up: 
61. Delete a resource: 
62. kubectl delete <resource_type> <resource_name> 
63.  
64. Delete all resources in a namespace: 
kubectl delete all --all -n <namespace> 
Errors in K8 & how to troubleshoot them 
Kubernetes, like any complex system, can encounter various errors and issues during 
setup, configuration, and runtime. Here are 20 common errors in Kubernetes and 
ways to troubleshoot them: 
1. Error: Unable to connect to the cluster 
Troubleshooting: 
• Verify your kubectl configuration using kubectl config view. 
• Ensure that the cluster API server is accessible from your machine. 
• Check if the cluster is running (kubectl cluster-info). 
2. Error: ImagePullBackOff or ErrImagePull 
Troubleshooting: 
• Verify the image name and repository. 
• Check image availability and permissions. 
• Ensure network connectivity to the container registry. 
3. Error: CrashLoopBackOff 
Troubleshooting: 
• Check pod logs (kubectl logs <pod_name>). 
• Inspect the pod's events (kubectl describe pod <pod_name>). 
• Verify resource constraints and application health. 
4. Error: PersistentVolumeClaim is pending 
Troubleshooting: 
• Check storage class availability and status. 
• Verify storage provider configuration. 
• Ensure sufficient storage capacity in the cluster. 
5. Error: Pod stays in Pending state 
Troubleshooting: 
• Check if there are enough resources in the cluster. 
• Inspect pod events and describe the pod (kubectl describe pod <pod_name>). 
• Examine the node's status and resource availability. 
6. Error: Service is not accessible 
Troubleshooting: 
• Verify service configuration and ports. 
• Check firewall rules and network policies. 
• Ensure that the service selector matches pod labels. 
7. Error: Unauthorized (RBAC-related issues) 
Troubleshooting: 
• Verify your user's RBAC permissions. 
• Check roles and role bindings (kubectl get roles, kubectl get rolebindings). 
• Ensure proper context and authentication settings in kubectl. 
8. Error: Node NotReady 
Troubleshooting: 
• Check if kubelet is running on the node. 
• Verify node status (kubectl get nodes). 
• Examine kubelet logs for errors. 
9. Error: Insufficient CPU or Memory 
Troubleshooting: 
• Check resource requests and limits in pod specs. 
• Verify node capacity and resource utilization. 
• Examine pod events and describe the pod. 
10. Error: NamespaceNotFound 
Troubleshooting: 
• Ensure the specified namespace exists. 
• Check your current context (kubectl config current-context). 
11. Error: ConfigMap or Secret not found 
Troubleshooting: 
• Verify the resource name and namespace. 
• Check if the resource was created (kubectl get configmaps). 
12. Error: DNS Resolution Issues 
Troubleshooting: 
• Verify CoreDNS or kube-dns pods are running. 
• Check DNS configuration in pods. 
• Ensure that the service and pod names are correct. 
13. Error: Invalid YAML Syntax 
Troubleshooting: 
• Use YAML linters to validate your configuration. 
• Double-check indentation and syntax. 
• Inspect error messages for specific details. 
14. Error: NodeSelector does not match nodes 
Troubleshooting: 
• Check node labels and selectors in pod specifications. 
• Verify that nodes match the required labels. 
15. Error: Unable to access external services 
Troubleshooting: 
• Check network policies and firewall rules. 
• Verify external service availability. 
• Examine service endpoint configurations. 
16. Error: ResourceQuota Exceeded 
Troubleshooting: 
• Check resource quotas and limits for namespaces. 
• Verify resource utilization in the cluster. 
17. Error: Ingress Controller Misconfiguration 
Troubleshooting: 
• Check Ingress resource for syntax errors. 
• Verify Ingress controller logs. 
• Ensure proper annotations and backend services. 
18. Error: Custom Resource Definition (CRD) Not Found 
Troubleshooting: 
• Check if the CRD is installed (kubectl get crds). 
• Verify API group and version. 
19. Error: Unable to create LoadBalancer Service 
Troubleshooting: 
• Verify cloud provider credentials. 
• Check if LoadBalancer services are supported in your environment. 
20. Error: Node Affinity or Anti-Affinity Issues 
Troubleshooting: 
• Check node affinity or anti-affinity rules in pod specifications. 
• Verify that nodes have the required labels. 
When troubleshooting Kubernetes issues, it's essential to use a systematic approach, 
inspect logs, and make use of Kubernetes resources like kubectl describe, kubectl 
logs, and kubectl get. Additionally, monitoring tools and observability solutions can 
provide insights into the cluster's health and performance. Always refer to the official 
Kubernetes documentation for detailed troubleshooting guidance.

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
### other exple pod with multi-container
```bash
apiVersion: v1
kind: Pod
metadata:
  name: redis-django
  labels:
    app: web
spec:
  containers:
    - name: key-value-store
      image: redis
      ports:
        - containerPort: 6379
    - name: frontend
      image: django
      ports:
        - containerPort: 8000
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
exple2
```bash
apiVersion: apps/v1 
kind: Deployment 
metadata: 
  name: example-deployment 
spec: 
  replicas: 3 
  selector: 
    matchLabels: 
      app: example 
  template: 
    metadata: 
      labels: 
        app: example 
    spec: 
      containers:
      - name: example-container 
        image: nginx:latest
```
• replicas: Number of desired replicas. 
• selector: Label selector to match pods controlled by this deployment. 
• template: Pod template with its own metadata and spec.

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
## A NodePort Service exposes the Service on each Node's IP at a static port. It makes the Service accessible externally by connecting to any Node's IP on the specified NodePort.
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
exmple 2 :  clusterIP
## A ClusterIP Service exposes the Service on an internal IP address within the cluster. 
## This type of Service is only reachable from within the cluster. 
```bash
apiVersion: v1 
kind: Service 
metadata: 
  name: example-service 
spec: 
  selector: 
    app: example 
  ports:
    - protocol: TCP 
      port: 80 
      targetPort: 8080
``` 
• selector: Label selector to define which pods the service targets. 
• ports: Port configuration to access the service.
exmple 3:LB
## A LoadBalancer Service automatically provisions an external load balancer in cloud environments (e.g., AWS, GCP) and assigns a public IP to the Service. It is useful for exposing services to the internet.
```bash
apiVersion: v1 
kind: Service 
metadata: 
  name: example-loadbalancer-service 
spec: 
  selector: 
    app: example 
  ports:
    - protocol: TCP 
      port: 80 
      targetPort: 8080 
type: LoadBalancer
```
exmple 4: ExternalName
## An ExternalName Service maps a Service to a DNS name. It is used for accessing external services by name.
```bash
apiVersion: v1 
kind: Service 
metadata: 
  name: example-externalname-service 
spec: 
  type: ExternalName 
  externalName: example.com
```
exemple 5: Headless Service 
## A Headless Service is used when you don't need load balancing or a single IP. It provides DNS resolution for the set of Pods but doesn't allocate a cluster IP. 
```bash
apiVersion: v1 
kind: Service 
metadata: 
  name: example-headless-service 
spec: 
  clusterIP: None 
  selector: 
    app: example 
  ports:
  - protocol: TCP 
    port: 80 
    targetPort: 8080
```
exemple 6:ingress
## While not a Service type per se, an Ingress is often used to expose HTTP and HTTPS routes to services within the cluster. It provides more advanced routing capabilities compared to basic Services.
```bash 
apiVersion: networking.k8s.io/v1 
kind: Ingress 
metadata: 
  name: example-ingress 
spec: 
  rules:
  - host: example.com 
    http: 
      paths:
      - path: /app 
        pathType: Prefix 
        backend: 
          service: 
            name: example-service 
            port: 
              number: 80
``` 
• rules: Define host-based routing. 
• http.paths: Specify path-based routing to services.

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
## Secrets in Kubernetes are used to store sensitive information, such as passwords or API keys. They can be mounted into pods as volumes or used as environment variables. 
```bash
apiVersion: v1 
kind: Secret 
metadata: 
  name: example-secret 
type: Opaque 
data: 
  username: YWRtaW4=  # base64-encoded 'admin' 
  password: cGFzc3dvcmQ=  # base64-encoded 'password'
```
• type: Opaque indicates a generic secret. 
• data: Base64-encoded key-value pairs.
## ConfigMaps allow you to decouple configuration artifacts from image content to keep containerized applications portable. 
```bash
apiVersion: v1 
kind: ConfigMap 
metadata: 
  name: example-configmap 
data: 
  app.config: | 
    key1: value1 
    key2: value2
```
• data: Key-value pairs representing the configuration.
## An Ingress in Kubernetes exposes HTTP and HTTPS routes from outside the cluster to services within the cluster. It allows external access to services. 
```bash 
apiVersion: networking.k8s.io/v1 
kind: Ingress 
metadata: 
  name: example-ingress 
spec: 
  rules:
  - host: example.com 
    http: 
      paths:
      - path: /app 
        pathType: Prefix 
        backend: 
          service: 
            name: example-service 
            port: 
              number: 80
``` 
• rules: Define host-based routing. 
• http.paths: Specify path-based routing to services.
### show containers run on backend
```bash
kubectl get daemonsets -n kube-system
```
### show health of cluster k8s
```bash
kubectl get componentstatuses
```

### -------------------------------------------------------rolling update -----------------------------------------------------
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
