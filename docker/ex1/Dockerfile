FROM python:3

RUN useradd --create-home test_user
USER test_user
WORKDIR /home/test_user

COPY hello.py .

CMD [ "python3", "hello.py" ]