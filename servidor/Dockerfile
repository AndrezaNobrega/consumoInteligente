FROM python:latest

ADD nuvem.py /servidor/
ADD client_secret.json /servidor/
ADD token.json /servidor/

EXPOSE 5000

WORKDIR /nuvem/

RUN pip install --upgrade pip
RUN pip install google-api-python-client
RUN pip install python-google-spreadsheet
RUN pip install google-auth
RUN pip install google-auth-oauthlib

CMD ["python3", "/nuvem/nuvem.py"]