FROM python:3.8
COPY controller_module/ /
COPY requirements.txt messageBroker.py /
WORKDIR /
RUN pip install -r requirements.txt

ENTRYPOINT ["python","main.py"]
