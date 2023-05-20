# Example 1

In this example we will use [ex1](../../docker/ex1) from the docker tutorial. We will show how, using Docker Compose, one can build a docker image and run a container based on that image. Compared to Docker, in Docker Compose, we have an additional file `docker-compose.yml` which will contain the needed information to build the image as well as the instructions to create and run a container from that image.

## Creating the Dockerfile
For a Docker Compose project, a Dockerfile is required which contains the needed instructions to build the Docker image.

The [`Dockerfile`](Dockerfile) contains the needed instruction to build an image to running a simple python script which prints "Hello world" to the screen. 
The reader may refer to [ex1](../../docker/ex1) from the docker tutorial for more information.

## Creating the docker-compose.yml file
With Docker Compose, the various instructions to build and create/run containers are encoded in a `docker-compose.yml` file.

At first we have
```
version: '3'
```
The [`version`](https://docs.docker.com/compose/compose-file/04-version-and-name/) top-level property is an infomartive statement which informs for which Docker Compose version the `docker-compose.yml` was written.

Next we have the services section:
```
services:

  hello:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-compose-tutorial/ex1
    container_name: ex1
```
The ['services'](https://docs.docker.com/compose/compose-file/05-services/) top-level property, introduces the various services defined within our Docker Compose application. As many services as needed can be defined in a same Docker Compose application. A service is an abstract definition of a computing resource which can be scaled/replaced independently from other components. In our case, we will have only one service, which is the Python application [`hello.py`](hello.py).


Each service has a name. In our case the name is `hello`. Within a service, various properties can be defined.

In our example we have a `build`, `image` and `container_name` property.

The [`build`](https://docs.docker.com/compose/compose-file/build/) property, specifies the build configuration for creating a Docker image from source. There are various ways to define these build instructions. In our example we choose an explicit one in which we define the [`context`](https://docs.docker.com/compose/compose-file/build/) and [`dockerfile`](https://docs.docker.com/compose/compose-file/build/) property. The `context` property defines either a path to a directory containing a Dockerfile, or a URL to a git repository. In our example we use the path `.`, which means we will use the same directory as the `docker-compose.yml` file to look for a `Dockerfile`. The `dockerfile` property allows to specify explicitly the name of the `Dockerfile`. In our example we could have sciped this property as per default Docker Compose looks for a `Dockerfile` named `Dockerfile`. There exists many more properties to configure the build process of the Docker image. Note that the [`build`] section is optional.

The [`image`](https://docs.docker.com/compose/compose-file/05-services/#image) section specifies the image to start the container from. The image is typically specified in the form `repository/tag`. If the image does not exist, Docker Compose will attempt to pull it, unless one has also specified `build` section, in which case it builds it using the specified options and tags it with the specified tag.

The [`container_name`](https://docs.docker.com/compose/compose-file/compose-file-v3/#container_name) property allows to specify a custom container name. In our case we use the name `ex1`.

## Creating and running a container
Once the `docker-compose.yml` file is defined, creating and running a container becomes simple and does not require, as with Docker, lengthy command lines. It becomes as simple as:
```
docker compose up 
```
Executing this command in the same directory where our `docker-compose.yml` file is stored will result in various actions, similar to this:
```
[+] Running 1/1
 ! hello Warning                                                                                  0.4s 
[+] Building 0.4s (9/9) FINISHED                                                                       
 => [internal] load .dockerignore                                                                 0.0s
 => => transferring context: 2B                                                                   0.0s
 => [internal] load build definition from Dockerfile                                              0.0s
 => => transferring dockerfile: 176B                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3                                       0.3s
 => [1/4] FROM docker.io/library/python:3@sha256:b9683fa80e22970150741c974f45bf1d25856bd76443ea5  0.1s
 => => resolve docker.io/library/python:3@sha256:b9683fa80e22970150741c974f45bf1d25856bd76443ea5  0.1s
 => [internal] load build context                                                                 0.0s
 => => transferring context: 29B                                                                  0.0s
 => CACHED [2/4] RUN useradd --create-home test_user                                              0.0s
 => CACHED [3/4] WORKDIR /home/test_user                                                          0.0s
 => CACHED [4/4] COPY hello.py .                                                                  0.0s
 => exporting to image                                                                            0.0s
 => => exporting layers                                                                           0.0s
 => => writing image sha256:c9982b56c3c74372acd7d41dcfcf8b8165264993e7432e14e5a30119029d02c5      0.0s
 => => naming to docker.io/docker-compose-tutorial/ex1                                            0.0s
[+] Running 2/0
 ✔ Network ex1_default  Created                                                                   0.0s 
 ✔ Container ex1        Created                                                                   0.0s 
Attaching to ex1
ex1  | Hello world
ex1 exited with code 0
```
As our docker image does not yet exist the first time we run `docker compose up`, Docker Compose will use the `build` section of our `docker-compose.yml` file to build the Docker image. It does this, using Docker and our `Dockerfile`.

In a second step, Docker Compose will create a container from our image and futher create a Docker Network for us. Once the container and the Network created, the contianer will run.

As expected, `Hello world` is displayed by our container `ex1`. Running `docker ps --all`:
```
CONTAINER ID   IMAGE                         COMMAND              CREATED         STATUS                     PORTS     NAMES
53781aa69a04   docker-compose-tutorial/ex1   "python3 hello.py"   4 seconds ago   Exited (0) 3 seconds ago             ex1
```
confirms that our container did run, and exited with no error.

## Removing a container
A container which was wired up by Docker Compose can be removed in a single command like so:
```
docker compose down
```
This command must be run in the same directory where our `docker-compose.yml` file is stored:
```
[+] Running 2/2
 ✔ Container ex1        Removed                                                                 0.0s 
 ✔ Network ex1_default  Removed                                                                 0.3s 
```
Note that the Docker Network is removed too. Running `docker ps --all`, confirms that our container was removed.

## Running an interactive container
As with Docker, it is possible to run a container in interactive mode using the [`docker compose run`](https://docs.docker.com/engine/reference/commandline/compose_run/) command. For our example this is achived like this:
```
docker compose run --rm hello bash
```
The option `--rm` will remove automatically the container once we exit it. The first argument of `docker compose run` is the name of the service, `hello` in our case, and the second argument the command to be executed, in our case `bash` in order to launch a bash shell. This command will override the command defined in the service configuration (in our case `pyhton3 hello.py`).

Running `docker compose run --rm hello bash` results in an interactive shell inside a container created based on our Docker image:
```
test_user@97c1b7c2ebc6:~$ 
```
As expected, the interactive shell is run by the user `test_user` as defined in the `Dockerfile`[Dockerfile]. Tu quite the runtime, the command `exit` has to be used. This results in automatic removal of the container, as we used the option `--rm`, as confirms the execution of `docker ps --all`.

## Cleaning up
At the end of this exercise it is a good practice to clean up our Docker. Check with `docker ps --all` that no undesired containers are present and remove them if needed with `docker rm`.

We can as well remove our Docker image we created with
```
docker image rm docker-compose-tutorial/ex1
```
With
```
docker image prune
```
you can as well remove any unused images.