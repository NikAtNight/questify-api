FROM python:3.12

LABEL maintainer="Nikhil Kapadia nikhil.kapadia.97@gmail.com"

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 80

COPY ./base.txt /code/base.txt
RUN pip install -r /code/base.txt

COPY docker/worker/supervisord.conf /etc/supervisord.conf

COPY . /code/
WORKDIR /code/

RUN mkdir /var/log/app

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
