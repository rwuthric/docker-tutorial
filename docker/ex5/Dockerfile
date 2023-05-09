FROM python:3

ARG UNAME=test_user
ARG UID=1100
ARG GID=1100

RUN groupadd --gid $GID $UNAME
RUN useradd --create-home --uid $UID --gid $GID $UNAME

USER $UNAME
WORKDIR /home/$UNAME
run mkdir logs

COPY server.py .

CMD [ "python3", "server.py" ]