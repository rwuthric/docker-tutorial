# Example 3
This example demonstrates how to include port mapping with Docker Compose. The [echo server](../../docker/ex3/echo.py) from [Example 3](../../docker/ex3) of the Docker tutorial is used for demonstration purpose.

## Creating the docker-compose.yml file
The Docker image is built based on the `Dockerfile` and `echo.py` from [Example 3](../../docker/ex3) of the Docker tutorial:
```
services:

  echo:
    build:
      context: https://github.com/rwuthric/docker-tutorial.git#:docker/ex3
      dockerfile: Dockerfile
    image: docker-compose-tutorial/ex3
    container_name: ex3
    ports: 
      - "6000:10000"
```
Port mapping is achieved with the [ports](https://docs.docker.com/compose/compose-file/compose-file-v3/#ports) directive. We used it here in the short form which takes the syntax `HOST:CONTAINER`, where `HOST` is the port on the Docker host which is mapped to the port `CONTAINER` in the container. In our example we have only one port mapping, but more can be added as needed.

## Creating and running a container
Creating the Docker image and wiring up a container is done the usual way, except that we add the [`--detach`](https://docs.docker.com/engine/reference/commandline/compose_up/) (short form `-d`) option in order to run our container in detached mode:
```
docker compose up -d
```
This command will build the image and run a container, named `ex3`, in detached mode as confirms `docker ps`:
```
CONTAINER ID   IMAGE                         COMMAND             CREATED          STATUS                   PORTS                                         NAMES
901bacc12543   docker-compose-tutorial/ex3   "python3 echo.py"   58 seconds ago   Up 57 seconds            0.0.0.0:6000->10000/tcp, :::6000->10000/tcp   ex3
```
Because of the `ports` directive in the `docker-compose.yml` file, the Docker host port `6000` maps indeed to port `10000` in the container. We can interact with the `echo.py` server from the Docker host:
```
telnet localhost 6000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
Hi
Hi
^]
telnet> quit
Connection closed.
```
Once the container is no longer needed, it can be stopped and removed with
```
docker compose down
```

## Cleaning up
At the end of this exercise it is a good practice to clean up Docker. Check with `docker ps --all` that no undesired containers are present and remove them if needed with `docker rm`.

The Docker image created during this exercise is removed with
```
docker image rm docker-compose-tutorial/ex3
```
And with
```
docker image prune
```
any unused images are removed.