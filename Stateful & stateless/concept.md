## Stateless is something that does not save inf about previous operations.Every time it carries each operation from the scrach just like the first time and provides functionnality such as web server, CDN ,or printing .

## Statefull saves information such as specific details of a user profile, preferences, and user actions" and permissions. This information is considered as the "status" of a system. Stateful applications typically involve some db , such SQL , MYSQ , or MongoDB and ps a read and/or write to it.

## a statefulSet is an object that mge a set of pods with unique identities. By assgning a persistent ID    that is maintained even if the pod is reschuduled.
## A statefulSet helps maintain the uniqueness and ordering of pods . with unique pod identities , administrators can efficiently attach cluster volumes to new pods across failures.
## A statefulSet controller deploys pods using similar specifications, pods are not interchangeable.
## StatefulSet does not creat a replicaSet such deployment
## the pod replicas cannot be rolled back to previous versions
## Statefulset are typically used for app thaat require persistent stge for stateful wrkloads, and ordered, automated rolling updates.

### so why not pvc ?
### pvc is shared accross the pods. if using a pvc all replicas will be using the some volume and none of it will have its own state.
### Statefulsets is used for stateful app, each replica of the pod will have its own state, and will be using its own volume.

## Components of a kubernetes statefulset :
### Statefulset : the template that defines pod selectors and replicas of containers that will run on the pods.
### Headless service; the net domain controller that allows clients to connect with pods using a DNS entry.
### Volume claim template: the template specification that alows administrators to provision stateful stge using persistent volumes.


## deployment is stateless par conter sttefulsets is stateful
## in deployment pods are assign an id that consists of the deployment name and a random hash to generate a temporaly unique identity. par contre in Same and a sequence number.
## in deployment pods are identical and can be interchanged par conter in statefulsets pods are neither indentical nor interchangeable
## in deployment a pod can be replaced by a new replica at any time par contre in statefulses pods retain their identity when rescheduléed on other node
## in deployment all replicas share a pvc and a volume par contre in statefulsets each pod get a unique volume and pvc 
## in deploy create svc par contre in statefulsets handle pods with headless service


### limitations of statefulsets
## there is no built-in way to resize volumes
## volumes are not deleted by default 
## Deleting a statefulSet does not guarantee that pods will terminate in order
## you have to manually create headless svc to benefit from reliable network identifiers