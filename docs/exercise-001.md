# Exercise 001 - Setting up the environment

This first exercise is for setting up the environment for devops experience workshop.

## Prerequisites

The following prerequisites are required for participating in this workshop.

- VirtualBox + extensions
- Git client (SSH enabled)
- Favorite editor
- 20GB of disk space
- 4GB of RAM
- Virtual machine image (provided), or can be build from the machine directory.

## Setting up the virtual machine

After the installation of VirtualBox, double-click on the provided image. The image will be imported and will be 
available in the VirtualBox interface. After importing the machine should be visible and can be started by 
right-clicking on the machine and selecting **start -> normal start**

![VM Setup]("images/vm-setup.png")

## After starting

After starting the DevOps platform becomes available. This platform is divided into three segments.

- Development (GIT server)
- Build/Deployment (Concourse)
- Run (blue/green deployment and ngnix)

![Training environment]("images/training-environment.png")

## Provide public SSH key

Provide a public SSH key that is used for git commits. Most of the time the this public key will be available at 
```$HOME/.ssh/id_rsa.pub```. Copy the contents of this key and paste it at the following location. 
[Upload SSH key](http://localhost:23238/). After submitting the platform will restart and will be available in a few 
seconds.

## Clone the GIT repository

The repository for the workshop can now be cloned. Used the following command.

```bash
$ git clone ssh://git@localhost:23237/git-server/repos/DevOpsTraining.git 
```

Now it is time to build the part of the continuous delivery pipeline.

