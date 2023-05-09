# Docker examples
This folder contains examples using docker

## Prerequisites
You need a machine with docker installed in it. You need a user account able to run docker.
In Ubuntu this means your user account must be part of the `docker` group.
You can check the membership of groups of your account like so:
```
id $USER
```
If you are not member of the docker group add it like so:
```
sudo usermod -aG docker <username>
```
where `<username>` is your user name. Be careful to use the correct option `-aG` (pay attention to case).

If you are not administrator on your machine, you will have to ask an administrator to add you to the docker group.

If you have only access to a windows machine, we recommend you install a virtual machine running Ubuntu (or any other distribution of Linux you like).


## Examples
- [Example 1](ex1) : Explains how to create a simple Dockerfile, a docker image and run docker containers
- [Example 2](ex2) : Explains how to create a Dockerfile in which some additional elements (in this case a python library) needs to be installed
- [Example 3](ex3) : Explains how to run a micro-service in a container and configure port mapping
- [Example 4](ex4) : Explains how to run two micro-services in two containers and enable them to talk to each others by attaching a docker network
- [Example 5](ex5) : Explains how to attach docker volumes to a docker container
