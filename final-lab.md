### Final Lab 
>  use the official documentation in case you need it


####Cluster setup
                
1. Configure your cluster to be working on kubernetes 1.21

####Kubernetes objects
                
1. Create a pod with nginx image, name it my-nginx, label it with type=front and app=app1
2. Create a replicaset based on the previously created my-nginx pod, it should have 7 replicas
3. Create a deployment based on httpd, name it mydeploy, it should have 3 replicas (use simplest way)
4. Configure a service to be listening on port 30008 for mydeploy
5. update mydeploy to use latest httpd image
6. scale mydeploy to use  replicas

####Taint & Labels
1. taint node1 with performance=high:NoSchedule
2. make the necessary changes to schedule pod/deployments on the master node
3. label node2 with disk=hdd
4. create a nginx pod that will be scheduled on node2 using nodeselector
5. Create a pod based on httpd
6. Do the necessary to kill the pod recently created without manual intervention.
7. list all nodes that has a linux os

####update cluster
1. update the cluster to be working on the latest version
