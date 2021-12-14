### LAB5 (NodeSelector) 
>  use the official documentation in case you need it

- Create a pod based on httpd, name it pod1, force it to be placed on node1.
- Create a pod based on nginx, name it pod2, force it to be placed on node2.
- Copy the following code, run it and do the necessary to fix it (Hint: it should expose the deployment on port 30009)
```bash
    apiVersion: v1
    kind: Pod
    metadata:
      name: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
      nodename: node1
```
