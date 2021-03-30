# Installation

Run a `git clone` command to get the latest version of the files. 
Create a new `config.ini` file by copying `config.sample.ini`. Enter your OpenWeatherMap API Key and save the file.

# Run using Docker

Build a new container image using the provided Dockerfile:
```
docker build -t ts3d-rainbow
```

Run a new container using the newly built container:
```
docker run --rm -d -p 8003:8003 ts3d-rainbow
```

The website is now available from the following URL: http://localhost:8003
