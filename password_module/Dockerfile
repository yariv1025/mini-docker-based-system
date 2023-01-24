FROM python:3.8
WORKDIR /app/

COPY requirements.txt message_broker.py /app/password_module/
COPY  configuration/ /app/configuration/
COPY services/ /app/password_module/services/
RUN pip install -r /app/password_module/requirements.txt

COPY password_module/ /app/password_module/

ENTRYPOINT ["python","/app/password_module/main.py"]
