## secret is sensitive information - login usernames and pwd , token , keys, etc - that is used within a kubernetes env.
## the primary purpose of  secrets is to reduce the risk exposing sensitive data while deploying applications on kubernetes.
## secrets have a size limit of 1 MB. When it comes to implementation, you can either mount Secrets as volumes or expose them as environment variables inside the pod manifest files.
## types of secrets
## opaque: this is the default type of secret. the secrets whose configuration file does not contain the type statement are all considered to be of this type.
## Service Account token : this store tokens identifying service accounts. Upon creation of a pod, kubernetes automatically creates this secret and associates it with the pod, enabling secure access to the API. this behavior can be disabled.
## basic authtication : these store basic authentication credentials, it must contain two key - username and password.
## SSH authentication :  For storing data necessary for establishing an SSH connection, this type's data field must contain an ssh-privatekey key-value pair.
## TLS : these Secrets store certificates and the associated keys used for TLS. You need to make sure the ts.key and the tls.crt keys are included in the data field of the secret's configuration.
## Docker config : this store the credentials for a specific Docker registry for container images.
## Bootstrap token : these are tokens used during the node bootstrap process, used to sign configmap.

### secrets are store in etcd and assign to pods such as volume or env.variables.