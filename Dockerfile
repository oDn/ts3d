FROM python:3.8.5

COPY . /app
WORKDIR /app

# Update and upgrade installed packages
RUN apt-get -y update
RUN apt-get -y upgrade
# Configure timezone
RUN ln -sf /usr/share/zoneinfo/Europe/Paris /etc/localtime
RUN dpkg-reconfigure -f noninteractive tzdata
# Upgrade pip and install project dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
# Create empty directory to store requests cache
RUN mkdir cache

EXPOSE 8003

ENTRYPOINT ["/app/gunicorn.sh"]
