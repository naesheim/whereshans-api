FROM python:alpine3.6
RUN mkdir /code
COPY . /code

WORKDIR /code
RUN pip3 install -r requirements.txt

ENTRYPOINT python3@
CMD app.py

