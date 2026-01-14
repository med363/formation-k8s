```bash
k apply -f simple-sts.yml
```
```bash
k apply -f mysql-sts.yml
```
### connect in mysql db in pod mysql
```bash
k get pod
```
```bash
k exec --stdin --tty db-mysql-0 --tty db-mysql-0 -- /bin/bash
```
```bash
mysql -u root -p 
```
# mge db 
```bash
create database hr;```

```bash
use hr; 
```

```bash
create table employees (emp id in AUTO INCREMENT , emp_name varchar(150) not null, primary key(emp_id)
)
```

```bash
show tables;
```

```bash
SELECT * FROM Employees;
```

```bash
INSERT INTO Employees(emp_name) value('Amine')
```

```bash
k scale sts db-mysql --replicas=2
```

```bash
k get all
```

```bash
k get pvc
```

```bash
k get pv
```

```bash
k get pvc
```

```bash
k exec --stdin --tty db-mysql-1 --tty db-mysql-1 -- /bin/bash
```

```bash
use hr;
```
## ==> not work !!!!!!! because statefulset not share pvc 
