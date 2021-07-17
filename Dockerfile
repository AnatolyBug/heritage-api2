# heritage-API Dockerfile

#Pull base image.
FROM python:3.9.5-slim

#Usefull to get logs
ENV PYTHONUNBUFFERED 1

#Make local dir
RUN mkdir -p /heritage-api2

#set "heritage-api" as the working directory
WORKDIR /heritage-api2

#https://luis-sena.medium.com/creating-the-perfect-python-dockerfile-51bdec41f1c8
COPY requirements.txt .

#now copy all the files in this directory to \code
ADD . .

#https://stackoverflow.com/questions/67444811/docker-unable-to-find-a-version-that-satisfies-the-requirement-mysqlclient-2
RUN set -eux && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

#pip install
RUN pip install -r requirements.txt

#Listen to port 5000 at run time
EXPOSE 8000

#start the app server
#CMD python manage.py runserver
CMD gunicorn --bind 0.0.0.0:8000 heritage.wsgi:application -k eventlet