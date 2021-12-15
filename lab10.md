
### LAB10 (Namespace) 
>  use the official documentation in case you need it

- Create 2 namespaces: dev and qual (via command line)
- Create  namespace prod (via cmanifest file)
- create a deployment named "deployment1" based on ubuntu/apache2 and place it on qual namespace.
- create a deployment named "deployment2" based on nginx and place it on prod namespace.
- Evict all pods from node2 (KEEP PODS WORKING, do the necessary!)
- Create a pod and place it in dev namespace (this namespace SHOULD be created automatically)
- Copy the following code and execute it, it is going to fail, I know :D , do the necessary to make it working.
```bash
    apiVersion: apps/v1
    kind: NameSpace
    metadata:
     name: demo-ns
      labels:
        name:demo-ns_environment
```
