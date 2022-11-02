FROM python:latest

ADD api.py /api/
ADD apiMetodos.py /api/
ADD apiTeste.py /api/
ADD templates/index.html /api/templates/
ADD static/css/app.css /api/static/css/
ADD static/js/app.js /api/static/js/

EXPOSE 5000

WORKDIR /api/

RUN pip install Flask
RUN pip install paho-mqtt
RUN pip install Flask-SocketIO

CMD ["python3", "/api/apiTeste.py"]
