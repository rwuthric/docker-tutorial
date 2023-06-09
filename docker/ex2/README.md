# Example 2
In this example we build a Dockerfile which requires some additional manipulations in order to configure our runtime. 

We want to run a Python script which gets the exchange rate from Canadian dollars to US dollars using the free API [ExchangeRate-API](https://www.exchangerate-api.com/).
The Python App [`currency.py`](currency.py) requires the Python package [`requests`](https://pypi.org/project/requests/), which according the documentation of the package can be installed with `pip` like so:
```
pip install requests
```
Further, the running container will connect to ExchangeRate-API in order to query the current exchange rate.

![Docker image and container](img/docker-ex2.png)

*Building a Docker image and wiring up a container*

## Creating the Dockerfile
If we use as starting image the [official Python image](https://hub.docker.com/_/python) on Docker Hub, the package `requests` will not be installed in it. We need to install it during the build process of our Docker image. For this we add
```
RUN pip install requests
```
in our `Dockerfile`. Note that we will install this package with the `test_user` and not the root user, which is the recommended practice. Except of this change, the rest of the `Dockerfile` is almost identical than the one from [example 1](../ex1).

## Building the docker image
With our `Dockerfile` ready, we can build an image. In the same path as your `Dockerfile`, execute
```
docker build -t docker-tutorial/ex2 .
```
which will result in something similar than this
```
[+] Building 13.1s (10/10) FINISHED                                                                                                                                                             
 => [internal] load build definition from Dockerfile                                                                                                                                       0.5s
 => => transferring dockerfile: 207B                                                                                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                                                                          0.4s
 => => transferring context: 2B                                                                                                                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3                                                                                                                                0.5s
 => [internal] load build context                                                                                                                                                          0.2s
 => => transferring context: 307B                                                                                                                                                          0.0s
 => CACHED [1/5] FROM docker.io/library/python:3@sha256:30f9c5b85d6a9866dd6307d24f4688174f7237bc3293b9293d590b1e59c68fc7                                                                   0.0s
 => [2/5] RUN useradd --create-home test_user                                                                                                                                              2.4s
 => [3/5] WORKDIR /home/test_user                                                                                                                                                          1.1s
 => [4/5] RUN pip install requests                                                                                                                                                         5.7s
 => [5/5] COPY currency.py .                                                                                                                                                               1.1s
 => exporting to image                                                                                                                                                                     1.5s 
 => => exporting layers                                                                                                                                                                    1.3s 
 => => writing image sha256:c799d61799c2f6840eef63e24de360e132895259aa82da1f9cd99935cea651b2                                                                                               0.1s 
 => => naming to docker.io/docker-tutorial/ex2 
```
Note that in step [4/5], the `requests` package is installed in the Docker image.

## Creating a container and running it
To create a container from our image and run it we use the [`docker run`](https://docs.docker.com/engine/reference/commandline/run/) command
```
docker run --rm docker-tutorial/ex2
```
which results in something similar than this
```
Today for 1 CAD you can buy  0.74447  USD
```
As we used the `--rm` option, the container is removed after exiting the container. You can verify it with `docker ps --all`.

It is interesting to note that the container was able to access the external URL, as would any other application running on your machine.

## Cleaning up
At the end of this exercise it is a good practice to clean up Docker. Check with `docker ps --all` that no undesired containers are present and remove them if needed with `docker rm`.

We can as well remove our Docker image we created. With
```
docker images
```
we can list images and clean up the ones we no longer need. For example the Docker image created during our tutorial is removed like so:
```
docker image rm docker-tutorial/ex1
```
With 
```
docker image prune
```
we remove any unused images.