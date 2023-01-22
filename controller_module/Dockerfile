FROM python:3.8
WORKDIR /app

COPY requirements.txt message_broker.py /app/controller_module/
RUN pip install -r /app/controller_module/requirements.txt

COPY  configuration/ /app/configuration/
COPY  controller_module/ /app/controller_module/

ENTRYPOINT ["python","/app/controller_module/main.py"]
