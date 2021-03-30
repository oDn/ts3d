FROM python:3.8.5

COPY . /app
WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade
RUN python3 -m pip install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["/app/gunicorn.sh"]
