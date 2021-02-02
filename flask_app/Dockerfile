FROM python:3.8-buster

LABEL MAINTAINER="Carlos Alberto Duarte Pinto <carlos.adpinto@gmail.com>"

ADD . /var/www
WORKDIR /var/www/
RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 8080

CMD ["gunicorn", "-w", "4", "--bind", "0.0.0.0:8080", "wsgi"]
