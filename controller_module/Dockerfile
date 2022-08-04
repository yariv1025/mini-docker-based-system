FROM python:3.8
COPY requirements.txt messageBroker.py /
COPY controller_module/ /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
