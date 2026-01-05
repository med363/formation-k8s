# sidecar Design pattern is a helper process such log files container that is not necessaire for run application in brief is an extra container in your pod to enhance or extend the functionaity of the main container.

# Adapter Design Pattern connect the main container with the external world.For example is a helper container that re-routes requests from the main container to the external world. This makes it possible for the main container to connect to localhost access , for example, an external db , but without any svc discovery. In brief is a container that transform output of the main container.


# Ambassador Design Pattern is a container that proxy the network connection to the main container


# hw it is communication inside a multi container pod , there are three ways that containers in the pod communicate with each other => shared nw ns(localhost), shared storage volumes (volume),shared ps ns (flag in yml files)

