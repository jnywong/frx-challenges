FROM python:3.12.5-slim-bullseye

RUN pip3 install gunicorn

RUN mkdir /opt/unnamed-thingity-thing

COPY . /opt/unnamed-thingity-thing

WORKDIR /opt/unnamed-thingity-thing

RUN pip3 install -r requirements.txt
