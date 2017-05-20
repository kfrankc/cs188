FROM ubuntu:16.04
ENV PYTHONUNBUFFERED 1

ENV HOME=/home/docker-dev
ENV WEB=$HOME/web
ENV PROJECT=$HOME/project

RUN apt-get update
RUN apt-get install -y python python-pip curl

RUN curl -sL https://deb.nodesource.com/setup_7.x | bash
RUN apt-get install -y nodejs

RUN mkdir -p $WEB
WORKDIR $WEB

ADD project/requirements.txt $WEB
RUN pip install -r requirements.txt \
  && rm requirements.txt

ADD web/package.json $WEB
# RUN chown -R docker-dev:docker-dev $HOME/*

RUN useradd -m docker-dev
# USER docker-dev
RUN npm install

# These will be overwritten with docker-compose volumes
COPY ./web $WEB
COPY ./project $PROJECT


CMD npm start
