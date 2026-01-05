# ds is a way to change or upgrade an application. the aim is to make the change without downtime / automate the whole updating process 
# rolling dep/default dep(dep progressive) replaces pods, one by one 
# maxSurge specifies the maximum number (or percentage) of pods above the specified number of replicas 
# maxUnavailabe declares the maximum number (or percentage) of unavailable pods during the update
# Recreate Update deployment shuts down all the old pods and replaces them with new ones such bank , asurances ...
# canary update Strategy is a partial update process that allows you to test 1:4 ratio your new program version on a real userbase without a commitment to a full rollout.
