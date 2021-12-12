### Prerequisites
2 or 3 Ubuntu 20.04 LTS System with Minimal Installation
Minimum 2 or more CPU, 3 GB RAM.
Disable SWAP on All node
SSH Access with sudo privileges



Server 1= master
Server 2= node1
Server 3= node2

- sudo hostnamectl set-hostname "master"
- sudo hostnamectl set-hostname "node1"
- sudo hostnamectl set-hostname "node2"

####Disable swap

- swapoff -a
- sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

Also comment out the reference to swap in /etc/fstab. Start by editing the below file:
- sudo nano /etc/fstab
- Reboot the system to take effect

- sudo reboot
####Update the system Packages

- sudo apt-get update

### Run these commands on Master/worker nodes

install below packages if not installed

```bash
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```
