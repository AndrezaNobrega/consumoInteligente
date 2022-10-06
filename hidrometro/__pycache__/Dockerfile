FROM python:latest

ADD hidroControl.py /hidrometro/
ADD hidrometro.py /hidrometro/

RUN pip install inputimeout

WORKDIR /hidrometro/

CMD ["python3", "/hidrometro/hidroControl.py"]