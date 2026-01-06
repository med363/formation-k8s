# the architecture of kubernetes stge is based on the abstraction of volumes. Volumes are defined as basic entities that containers can use to access stge in kubernetes. they can be mounted on different storage infrastructure types, whether it's local storage devices, NFS , and cloud storage service.
# volumes in kubernetes can be accessed directly in two ways. Ephemeral/non-persistent volumes can be used for short-term (test ,dev.....)storage, whereas persistent volumes are defined for long*term/ permanent storage.
# non-persistent storage by deft , k8s storage is temp (non-persistent). Any stge defined as part of a container in kubernetes pod, is held in the host's temp storage space , wich eists as long as the pod exists, and is then removed. Container storage is portable, but not durable.
# pS k8s also support a variety of persistent storage models, including files, block storage, object storage, and cloud services belonging to these and additional categories. stge can be referenced directly from within a pod, but this violates the pod's portability principles and is not recommended. Instead, pods should use persistent volumes and persistent volume claims (PV/PVC) to define the storage requirement of their applications.
# PV is a piece of storage in a cluster that an administrator has provisioned. It is a rs in the cluster, just as a node is a cluster rs.A pv is a volume plug-in  that has a lifecycle ind of any ind pod that uses the pv.
# A pvc is a request for storage by a user.It is similar to a pod. pods consume node rs and PVCs consume PV rs.Pods can request specific levels of rs (CPU and Memory). Claims can request specific size and access modes (e.g., they can be mounted ReadWriteOnce, ReadOnlyMany or ReadWriteMany, see AccessModes).
```bash
kubectl explain pod.spec.volumes
```
```bash
kubectl explain pod
```
```bash
kubectl explain deployment
```
