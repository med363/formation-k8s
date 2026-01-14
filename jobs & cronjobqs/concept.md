
## Ajob creates one or more pods AND will continue to  retry execution of the pods until a specified number of them succesfully terminate. As pods successfuly complete, the job tracks the successful compleeetions.when a specified number of successful completions is reached, the job is complete.
## Deleting a job will clean up the pods it created. Suspending a job will delete its active pods until the job is resumed again.
## you can also use a job to run multiple pods in //.
## 3 types // jobs:
# non // jobs (backup).
# // jobs with a fixed completion count => these jobs occur concurrently, but run a set amount of times before terminating succesfully. By setting .spec.completions to a value greater than one, you trigger the formation of succesful pods. you may also add an index to these jobs, meaning that each pod is assigned a portion of the overall task to complete.
# // jobs with a work queue ==> this involves running multiple jobs concurrently, or in // . In many instances, it's not practical to allow one job to finish before starting another one. // ps is highly efficient and favorable when computer resources adequately support them.