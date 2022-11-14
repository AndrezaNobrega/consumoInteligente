FROM python:latest

ADD apiMetodos.py /apiRest/
ADD api.py /apiRest/
ADD telas.py /apiRest/

EXPOSE 5000

WORKDIR /apiRest/

RUN pip install Flask
RUN pip install paho-mqtt
RUN pip install Flask-SocketIO
RUN pip install requests

CMD ["python3", "/apiRest/api.py"]
