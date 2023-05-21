# Example 2
In this example we show how a docker image can be built from a `GitHub` repository.

## Creating the docker-compose.yml file
As we will obtain all information required to build our Docker image from a `GitHub` repository, we need only to define the `docker-compose.yml` file.

In our case, we want to create a Docker image based on [Example 1](../ex1) from our Docker Compose tutorial. The important lines in the `docker-compose.yml` file are
```
build:
  context: https://github.com/rwuthric/docker-tutorial.git#:docker-compose/ex1
  dockerfile: Dockerfile
```
As context we use the `GitHub` public URL (https://github.com/rwuthric/docker-tutorial.git in our case). As further all the information is within the sub-folder `docker-compose/ex1` of our repository, we add `#:docker-compose/ex1` behind the public URL as explained in more details in the official [Docker Compose documentation](https://docs.docker.com/engine/reference/commandline/build/#git-repositories).

In more details: `#` tells Docker that context configuration will start. A semicolon `:` is used to separate the two parts of the context configuration. As first part is provided the branch or tag one whishes to checkout. We leave it empty as we want to use the main branch (we could have written `#main:docker-compose/ex1` to be more explicit). The second part represents a subdirectory inside the repository that will be used as a build context (which is `docker-compose/ex1` in our case).

## Creating and running a container
Creating the Docker image and wiring up a container is done the usual way:
```
docker compose up
```
which will pull the repository into a temporary directory, which is afterwards used to build the Docker image:
```
+] Running 1/1
 ! hello Warning                                                                                                         0.3s 
[+] Building 2.1s (7/7) FINISHED                                                                                              
 => [internal] load git source https://github.com/rwuthric/docker-tutorial.git#:docker-compose/ex1                       1.9s
 => [internal] load metadata for docker.io/library/python:3                                                              0.1s
 => [1/4] FROM docker.io/library/python:3@sha256:b9683fa80e22970150741c974f45bf1d25856bd76443ea561df4e6fc00c2bc17        0.1s 
 => => resolve docker.io/library/python:3@sha256:b9683fa80e22970150741c974f45bf1d25856bd76443ea561df4e6fc00c2bc17        0.1s 
 => CACHED [2/4] RUN useradd --create-home test_user                                                                     0.0s 
 => CACHED [3/4] WORKDIR /home/test_user                                                                                 0.0s 
 => CACHED [4/4] COPY hello.py .                                                                                         0.0s
 => exporting to image                                                                                                   0.0s
 => => exporting layers                                                                                                  0.0s
 => => writing image sha256:b9cdf034de75162bbd8a590a4131d89bbf7fb07973ecb3a1a60a6f385133c81d                             0.0s
 => => naming to docker.io/docker-compose-tutorial/ex2                                                                   0.0s
[+] Running 1/1
 ✔ Container ex2  Created                                                                                                0.0s 
Attaching to ex2
ex2  | Hello world
ex2 exited with code 0
```

## Removing the container
The created container and Docker Network is removed in a single command the usual way:
```
docker compose down
```
Running `docker ps --all`, confirms that our container was removed.

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