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

#https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/
RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev

RUN pip install -r requirements.txt

#CMD python manage.py runserver
CMD gunicorn --bind 0.0.0.0:8000 heritage.wsgi:application -k eventlet