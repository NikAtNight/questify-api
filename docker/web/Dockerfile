FROM python:3.12

LABEL maintainer="Nikhil Kapadia nikhil.kapadia.97@gmail.com"

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./base.txt /code/base.txt

RUN pip install --upgrade pip
RUN pip install -r /code/base.txt

COPY . /code/
WORKDIR /code

COPY docker/web/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
