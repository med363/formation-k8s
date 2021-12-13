
### LAB3 (Deployment) 
>  use the official documentation in case you need it

- Create a deployment based on httpd, with 6 replicas, name it deployment-httpd, keep record of the changes.
- Create a deployment based on nginx with the following labels: version=v1 and type=front, name it my-deploy.
- Pick any deployment and scale it up to 9 (via the manifest file)
- update the used image in deployment-httpd to be 2-alpine3.15
- do a rollback of the last change.
- Copy the following code, run it and do the necessary to fix it
```bash
    apiVersion: v1/apps
    kind: deployment
    metadata:
      name: deployment1
      labels:
        version: v1
    spec:
      selector:
        matchLabels:
          type: webserverX
      template:
        metadata:
          name: nginx
          labels:
            type: webserverY
        spec:
          containers:
          - name: nginx
            image: nginx:1.14.2
      replicas: 5
```

