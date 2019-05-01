FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install ffmpeg -y && \
    apt-get install awscli -y

WORKDIR /tmp/workdir

COPY entrypoint.sh /tmp/workdir 

ENTRYPOINT ./entrypoint.sh
