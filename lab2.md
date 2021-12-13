### LAB2 (ReplicaSet) 
>  use the official documentation in case you need it
- Create a replicaset based on httpd, with 6 replicas
- Create a replicaset with the following labels: version=v1 and type=front
- Pick any replicaset and scale it up to 9 (via the manifest file)
- Scale down the previous replicaset into 2 ( via the command line tool)
- Scale down the previous replicaset into 5 ( via the command line tool + manifest)

- Copy the following code, run it and do the necessary to fix it
```bash
    kind: Replicaset
    apiVersion: apps/v1
    metadata:
      name: my-rc
      labels:
        type: front-end
    spec:
      template:
        metadata:
          name: nginx
          labels:
            type: front
        spec:
          containers:
          - name: nginx
            image: nginx:1.14.2
      replicas: 5
      selector:
        matchLabels:
          type: back
```
