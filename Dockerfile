FROM python:3.12.5-slim-bullseye

RUN apt update -qq && \
    apt install --yes tini && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install gunicorn

RUN mkdir /opt/frx-challenges

COPY requirements.txt /tmp/requirements.txt
RUN python -m pip install -r /tmp/requirements.txt

COPY . /opt/frx-challenges

WORKDIR /opt/frx-challenges/frx_challenges

ENTRYPOINT ["tini", "--"]
