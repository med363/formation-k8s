### LAB7 (Taints & Tolerations) 
>  use the official documentation in case you need it

- Taint node1 one with color=white, disk=ssd, perf=strong
- Taint node2 one with color=black,  perf=weak
- Create a pod based on nginx, this pod MUST be deployed on a server with weak performance.
- Copy the following code, run it and do the necessary to fix it.
```bash
    apiVersion: v1
    kind: Pod
    metadata:
      name: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
      tolerations:
        - key: "color"
          value: "white"
          effect: "NoSchedule"
```
