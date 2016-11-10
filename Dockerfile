FROM python:2.7
MAINTAINER Grace Wong <grace@getclef.com>

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
