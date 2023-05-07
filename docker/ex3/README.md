# Example 3
This example shows how to build a docker image with a micro-service in it, how to run, stop and remove a container based on this image.

The micro-service from this example will require port mapping in order to be accessible from the host running docker. This aspect will be introduced during this example.

## Echo server
The docker image we want to build will run a micro-service in form of a simple python echo server. The [echo server](echo.py) listens to port `10000` on the `localhost` for incoming connections. 

Once a client connects to it, it will echo back to the client and data sent to the echo server.

You can try out the server by running it:
```
python echo.py
```
In a different terminal on your machine running the echo server, you can open a `telnet` session connecting to the localhost on port `10000`:
```
telnet localhost 10000
```
which will result in
```
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
```
You can now send data to the echo server, and the echo server will sent it back to you:
```
telnet localhost 10000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
This is a test
This is a test
```
To quit telnet press the `Ctrl` key together with the `]` key and type exit on the prompt.
```
telnet localhost 10000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
This is a test
This is a test
^]
telnet> quit
Connection closed.
```
To stop our echo server you will have to interrupt its execution with Ctrl-C.

Important note: Note that in `echo.py` the server is setup like this:
```
server_address = ('0.0.0.0', 10000)
```
which means the server will bind to `0.0.0.0` which means it binds to all interfaces. This will be key in order we can connect to the server from outside a docker container.

## Creating and building the Dockerfile
The `Dockerfile` is essentialy the same as the one from [example 1](../ex1). Only difference is we use `echo.py` as python file we want to have isnide our docker image. The image is built the usual way:
```
docker build -t docker-tutorial/ex3
```

## Running the service in detached mode
As our echo server will run indefinitely, we do not want to run the service in the so called detached mode where the docker container will be run in the background. This is achieved like so:
```
docker run --rm --name ex3 -d docker-tutorial/ex3 
```
where we used the `--detach` (short `-d`) option. Executing `docker ps` confirms our container is up and running:
```
CONTAINER ID   IMAGE                 COMMAND             CREATED         STATUS         PORTS     NAMES
312e055c2e2e   docker-tutorial/ex3   "python3 echo.py"   5 seconds ago   Up 4 seconds             ex3
```
If you wish to stop the container you can use the [`docker stop`](https://docs.docker.com/engine/reference/commandline/stop/) command:
```
docker stop ex3
```
As we did run the container with the `--rm` option, it got automatically removed as confirms `docker ps --all`.

## Port mapping
You may ask how can we connect to our echo server inside our container? Of course an attempt like  `telnet localhost 10000` will fail as no server is unning on port `10000` on our machine. In order to access our echo server isnide the container we need to forward port `10000` to some port on our machine. This can be achieved with the `--publish` (short `-p`) option when running the container like so:
```
docker run --rm --name ex3 -d -p 6000:10000 docker-tutorial/ex3
```
This will forward port `6000` from the host to port `10000` in the container. In docker this is called port mapping. More documentation can be found [here](https://docs.docker.com/config/containers/container-networking/).

The `docker ps` command shows the mapped port:
```
CONTAINER ID   IMAGE                 COMMAND             CREATED         STATUS         PORTS                                         NAMES
f128f784fabd   docker-tutorial/ex3   "python3 echo.py"   8 seconds ago   Up 6 seconds   0.0.0.0:6000->10000/tcp, :::6000->10000/tcp   ex3
```
It is now possible to connect to the echo server inside the container like this:
```
telnet localhost 6000
```
Because of the option `-p 6000:10000` we used in `docker run`, the traffic of port `6000` is forward to port `10000` inside the container, where the echo server is listening.


## Cleaning up
At the end of this exercise it is a good practice to clean up our docker. Check with `docker ps --all` that no undesired containers are present and remove them if needed with `docker rm`.

We can as well remove our docker image we created. With
```
docker images
```
we can list our images and clean up the ones we no longer need. For example the docker image created within our tutorial:
```
docker image rm docker-tutorial/ex3
```
With 
```
docker image prune
```
you can as well remove any unused images.