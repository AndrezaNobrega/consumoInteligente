FROM python:latest

ADD apiMetodos.py /api/
ADD apiTeste.py /api/
ADD telas.py /api/
ADD templates/index.html /api/templates/
ADD static/css/app.css /api/static/css/
ADD static/js/app.js /api/static/js/

EXPOSE 5000

WORKDIR /api/

RUN pip install Flask
RUN pip install paho-mqtt
RUN pip install Flask-SocketIO
RUN pip install requests

CMD ["python3", "/api/apiTeste.py"]
