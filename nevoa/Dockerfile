FROM python:latest

ADD noNevoa.py /nevoa/
ADD dadosGerais.xlsx /nevoa/
ADD historicoGeralNo.xlsx /nevoa/
ADD pagamentos.xlsx /nevoa/


EXPOSE 1883

WORKDIR /nevoa/

RUN pip install paho-mqtt
RUN pip install pandas
RUN pip install o openpyxl

CMD ["python3", "/nevoa/noNevoa.py"]