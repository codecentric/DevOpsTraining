# DevOps training vagrant machine

Machine for running the DevOps training

## Prerequisites

- Vagrant
- VirtualBox
- Vagrant disk plugin


## Getting started

- Install required Ansible packages ```bash $ sudo ansible-galaxy install -r requirements.yml``` (Makes docker 
installation available on host machine)
- Install vagrant disk plugin ```bash $ vagrant plugin install vagrant-disksize```
- Start the machine with ```bash $ vagrant up```
