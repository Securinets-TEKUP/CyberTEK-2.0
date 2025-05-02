FROM ubuntu:latest

RUN apt-get update && apt-get install -y socat
RUN apt-get install -y cpulimit


WORKDIR /app

RUN useradd -m ctf

COPY main main.c flag.txt ./
RUN chmod +x main

USER ctf

EXPOSE 10001

CMD socat TCP-LISTEN:10001,reuseaddr,fork EXEC:'./main'