FROM python:latest

ADD noNevoa.py /nevoa/

EXPOSE 1883

WORKDIR /nevoa/

RUN pip install paho-mqtt
RUN pip install pandas

CMD ["python3", "/nevoa/noNevoa.py"]