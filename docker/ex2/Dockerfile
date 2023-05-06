FROM python:3

RUN useradd --create-home test_user
USER test_user
WORKDIR /home/test_user

RUN pip install requests
COPY currency.py .

CMD [ "python3", "currency.py" ]