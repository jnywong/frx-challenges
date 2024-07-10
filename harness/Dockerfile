FROM python:3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache -r /tmp/requirements.txt

COPY longest.py /opt/longest.py

ENTRYPOINT ["python3", "/opt/longest.py"]