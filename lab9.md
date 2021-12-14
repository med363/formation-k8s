### LAB9 (Drain // uncordon) 
>  use the official documentation in case you need it

- Create a deployment based on nginx, it shoudl have 12 replicas, name it my-deployment

For maintenance purpose, we need to upgrade some critical packages on the worker node1 and node2.

- Evict all pods created on node1
- Check where these pods are placed ?
- Evict all pods from node2 (KEEP PODS WORKING, do the necessary!)
- Maintenance on node1 and node is finished. Make them available again.
- Apply the best practise in this case ( think about master!).
