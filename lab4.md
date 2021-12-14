
### LAB4 (Services) 
>  use the official documentation in case you need it

- Create a deployment based on httpd, with 6 replicas, name it deployment-httpd.
- Create a nodePort service that expose our previously created deployment on port 30008.
- Copy the following code, run it and do the necessary to fix it (Hint: it should expose the deployment on port 30009)
```bash
    apiVersion: apps/v1
    kind: service
    metadata:
      name: myapp-service
    spec:
      type: NodePort
      ports:
      - targetPort: 80
        port: 80
        nodePort: 30009
      selector:
        type: webserver
```

