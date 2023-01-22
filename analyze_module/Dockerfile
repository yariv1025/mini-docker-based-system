FROM python:3.8
WORKDIR /app/

COPY requirements.txt message_broker.py /app/analyze_module/
RUN pip install -r /app/analyze_module/requirements.txt

COPY services/ /app/analyze_module/services/
COPY  configuration/ /app/configuration/
COPY analyze_module/ /app/analyze_module/

ENTRYPOINT ["python","/app/analyze_module/main.py"]
