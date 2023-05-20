# Docker-compose examples
This folder contains examples using docker-compose

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

If you have access only to a windows machine, we recommend you install a virtual machine running Ubuntu (or any other distribution of Linux you like).


## Examples
- [Example 1](ex1) : Explains how to create a simple Docker Compose application