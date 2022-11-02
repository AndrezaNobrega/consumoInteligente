FROM python:latest

ADD hidrometro.py /hidrometro/
ADD hidroPublisher.py /hidrometro/

RUN pip install paho-mqtt

WORKDIR /hidrometro/

CMD ["python3", "/hidrometro/hidroPublisher.py"]
