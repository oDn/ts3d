FROM python:3.8.5

COPY . /app
WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 8003

ENTRYPOINT ["/app/gunicorn.sh"]
