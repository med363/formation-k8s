
### LAB8 (Node Selector) 
>  use the official documentation in case you need it

- Add new label to node1  with size=large
- Add new label to node2  with size=medium
- Copy the following code, run it and do the necessary to fix it (it should be placed on the node with minimum size).
```bash
    apiVersion: apps/v1
    kind: Pod
    metadata:
      name: nginx
    spec:
      containers:
      - name: nginx-container
        image: nginx
      nodeSelector:
          size: small
```
