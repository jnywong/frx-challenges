FROM python:3.12.5-slim-bullseye

RUN apt-get update && apt-get install -y git

RUN pip3 install gunicorn

RUN git clone https://github.com/2i2c-org/unnamed-thingity-thing /opt/unnamed-thingity-thing
WORKDIR /opt/unnamed-thingity-thing

RUN pip3 install -r requirements.txt
