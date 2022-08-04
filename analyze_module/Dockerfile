FROM python:3.8
COPY analyze_module/ /
COPY requirements.txt messageBroker.py /
COPY services/ /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
