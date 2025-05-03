FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY ./challenge /challenge
RUN chmod +x recall ld-linux-x86-64.so.2 libc.so.6

RUN useradd -m ctfuser
COPY ./flag.txt /challenge
RUN chmod 444 /challenge/flag.txt
RUN chmod -w /challenge
USER ctfuser

EXPOSE 6004

CMD ["socat", "TCP-LISTEN:6004,reuseaddr,fork", "EXEC:/challenge/ld-linux-x86-64.so.2 --library-path /challenge /challenge/recall,stderr"]
