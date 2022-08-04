FROM python:3.8
COPY requirements.txt messageBroker.py /
COPY analyze_module/ /
COPY services/ /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
