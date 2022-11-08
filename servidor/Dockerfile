FROM python:latest

ADD servidor.py /servidor/
ADD vazamento.xlsx /servidor/

EXPOSE 1883

WORKDIR /servidor/

RUN pip install paho-mqtt
RUN pip install pandas

CMD ["python3", "/servidor/servidor.py"]