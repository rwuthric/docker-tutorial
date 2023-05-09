# Example 5
This example shows how to build a docker image with a micro-service which waits for connections and logs them into a file. We will discuss how to attach docker volumes to a container in order the log file can be kept even the container gets removed.

# TCP/IP server
In this example we run a mini server which listens to port `10000`. Whenever a connection happens, it sends a greeting message to the client and logs in the file `log.txt` (which is int he folder `logs`) the time, IP and port of the connection.

Before trying your server, you need to create a folder `logs` which will contain the `log.txt` file:
```
mkdir logs
```
You can now try out the server by running it:
```
python server.py
```
In a different terminal on your machine running the echo server, you can open a telnet session connecting to the localhost on port 10000:
```
telnet localhost 10000
```
which will result in
```
trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Welcome
To quit type "bye".
```
Typing `bye` will close the connection to the server. You will note that a file `log.txt` was created inside the 'logs' directory and contains an entry similar to this (run for example `cat logs/logs.txt`):
```
[2023-05-09 10:25:08] ('127.0.0.1', 57088)
```
Before continuing you can remove the `log.txt` file with
```
rm logs/log.txt
```

# Creating and building the Dockerfile
The Dockerfile contains several new elements compared to [example 1](../ex1). Besides using the `server.py` as file we want to copy inside our docker image, there are some new directives which you may be unfamiliar with. We will explain them later. For the moment, create the image the usual way:
```
docker build -t docker-tutorial/ex5 .
```

# Running the service
To create and run a container from our image we proceed like so:
```
docker run --rm --name ex5 -d -p 6000:10000 docker-tutorial/ex5
```
Here we map prot `10000` from the container to port `6000` of our host running docker. As expected we can connect to our service with `telnet localhost 6000`. However, no entries in the file `log.txt` can be found. In fact even no `log.txt` file is created at all.

The file `log.txt` is indeed created and populated, but inside our running container. We can verify this by connecting to our running container like so:
```
docker exec -it ex5 bash
```
The [docker exec](https://docs.docker.com/engine/reference/commandline/exec/) command executes a command in a running container. In our case we execute the command `bash`, which opens a bash shell in our container `ex5`. With the options `-it` we run it interactively and attach a pseudo-`TTY`.

Inside the runtime, we can confirm that the `log.txt` file exists (with `ls logs`) and it gets populated (`cat logs/log.txt`).

# Attaching a docker volume to a container
Docker allows to mount volumes inside containers. Several types of volumes exist and several ways on how they are mounted. A detailed description can be found in the official [documentation on docker volumes](https://docs.docker.com/storage/volumes/). In this example we will use the `--volume` (short `-v`) option when creating and running the container to attach a volume to the container:
```
docker run --rm --name ex5 -v ./logs:/home/test_user/logs -d -p 6000:10000 docker-tutorial/ex5
```
The `--volume` option is used in the format like 
```
--volume host/directory:/container/directory
```
Note that the container paths must always be absolute paths, whereas host paths can be either absolute paths or relative paths to the current working directory (from where you start your `docker run` command). In our example we attach the host directory `./logs/` (the one we created at start of our tutorial) to he container directory `/home/test_user/logs`.

Let us check if we can connect to our service and log our connection to the `log.txt` file:
```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Connection closed by foreign host.
```
Obviously something must have gone wrong. We connected to our service, but it was right away closed. The `docker ps --all` command further shows that the container `ex5` was removed.

To understand what did happen, lets run our container interactively:
```
docker run --rm  -v ./logs:/home/test_user/logs -it -p 6000:10000 docker-tutorial/ex5
```
In a second terminal on our host, let us try to connect to our service inside the container with `telnet localhost 6000`. In our container we obtain the following output:
```
Starting TCP/IP server on 0.0.0.0 port 10000
Waiting for a connection ...
Connection from ('172.17.0.1', 53572)
Traceback (most recent call last):
  File "/home/test_user/server.py", line 32, in <module>
    with open("logs/log.txt", "a") as logfile:
         ^^^^^^^^^^^^^^^^^^^^^^^^^
PermissionError: [Errno 13] Permission denied: 'logs/log.txt'
```
We can observe that the server did indeed start, was waiting for a connection. Once a connection is received, an error occurs with is a `PermissionError` on the file `logs/log.txt`. Seems we can not write anymore to our file. Why is this so?

To understand the problem, let us start the container again in detached mode:
```
docker run --rm  --name ex5 -v ./logs:/home/test_user/logs -d -p 6000:10000 docker-tutorial/ex5
```
and let’s connect to our running container:
```
docker exec -it ex5 bash
```
Exectuing inside our container `ls -l` shows the problem:
```
test_user@2dab5377e2f6:~$ ls -l
total 8
drwxr-xr-x 2 1001 1001 4096 May  9 15:47 logs
-rw-r--r-- 1 root root 1488 May  9 15:18 server.py
```
You may get different UID and GID for the owner of the `logs` folder. In fact, it is the UID and GID of the user which is running the docker commands. But our `test_user` in the container has different UID and GID:
```
test_user@2dab5377e2f6:~$ id test_user
uid=1100(test_user) gid=1100(test_user) groups=1100(test_user)
```
The UID=1100 and GID=1100 are the values we did choose in the `Dockerfile`. Our `Dockerfile` has these directives:
```
ARG UNAME=test_user
ARG UID=1100
ARG GID=1100

RUN groupadd --gid $GID $UNAME
RUN useradd --create-home --uid $UID --gid $GID $UNAME
```
First, we define three [ARG](https://docs.docker.com/engine/reference/builder/#arg) instructions. An ARG instruction defines a variable that can be used later in the `Dockerfile`. It can further be overwritten during the `docker build` process as we will discuss soon. 

With the linux commands `groupadd` and `useradd`, we create a group which has a GID of `1100` (the value we defined in `ARG GID=1100`) and the name of the group will be `test_user` (the value we defined in `ARG UNAME=test_user`), and we create a user with UID `1100` (the value defined in `ARG UID=1100`) and GID `1100` (the value we defined in `ARG GID=1100`). At the same time we create as well the home directory of that user.

Now, when we attach our local directory `./logs` from our host, the owner of that directory becomes the user running the docker command. This user will in general not have a UID of `1100` and a GID of `1100`. In the example displayed here, the user had actually a UID of `1001` and a GID of `1001`.

In order the `test_user` has write acces to the attached folder `logs`, it has to have the same UID and GID than the user running the docker command. We could simply change our `Dockerfile` with the desired values. But docker offers a better solution. We can actually overwrite the variables defined with `ARG` directive at the moment we build our docker image. In our case we can do this like so. First we need to stop our running container
```
docker stop ex5
```
Then we want to remove our image as we want to rebuild it fresh:
```
docker image rm docker-tutorial/ex5 
```
We can now rebuild it, but passing the build arguments `UID` and `GID`:
```
docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t docker-tutorial/ex5 .
```
The option [`--build-arg`](https://docs.docker.com/engine/reference/commandline/build/#build-arg) allows to overwrite any `ARG` directive from the `Dockerfile`. In our case we overwrite two of them: UID and GID. We use the Linux command `id -u` to obtain the UID of our user and the command `id -g` to obtain the GID of our user.

Let us create and run a container from our image:
```
docker run --rm  --name ex5 -v ./logs:/home/test_user/logs -d -p 6000:10000 docker-tutorial/ex5
```
and lets connect to our running container:
```
docker exec -it ex5 bash
```
Executing inside our container `ls -l` shows
```
test_user@31ccb46a6ffb:~$ ls -l
total 8
drwxr-xr-x 2 test_user test_user 4096 May  9 15:47 logs
-rw-r--r-- 1 root      root      1488 May  9 15:18 server.py
```
This time the `logs` folder belongs to the `test_user` as this user has the same UID and GID as the user running the docker container. Let us exit the container with `exit`.

As `test_user` has now write access to the folder `logs`, we can connect from our host (`telnet localhost 6000`) as expected. Further, `cat logs/log` on the host shows that the logs from `server.py` running inside the container are stored on the local folder `./logs` of the host.

## Cleaning up
At the end of this exercise it is a good practice to clean up our docker engine. Check with `docker ps --all` that no undesired containers are present and stope them if needed with `docker stop`. This will most likely be
```
docker stop ex5
```
We can as well remove our docker image we created with
```
docker image rm docker-tutorial/ex5
```
With 
```
docker image prune
```
you can as well remove any unused images.
