FROM ubuntu:16.04
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y python python-pip curl

RUN curl -sL https://deb.nodesource.com/setup_7.x | bash
RUN apt-get install -y nodejs

RUN mkdir /home/docker-dev
WORKDIR /home/docker-dev

ADD project/requirements.txt /home/docker-dev
RUN pip install -r requirements.txt

ADD web/package.json /home/docker-dev
RUN npm install


RUN useradd -m docker-dev
USER docker-dev

# These will be overwritten with docker-compose volumes
COPY ./web /home/docker-dev/web
COPY ./project /home/docker-dev/project

CMD npm start --prefix /home/docker-dev/web
