FROM python:3.8
WORKDIR /app

COPY requirements.txt message_broker.py /app/controller_module/
COPY  configuration/ /app/configuration/
RUN pip install -r /app/controller_module/requirements.txt

COPY  controller_module/ /app/controller_module/

ENTRYPOINT ["python","/app/controller_module/main.py"]
