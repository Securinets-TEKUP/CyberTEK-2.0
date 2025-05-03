FROM ubuntu:18.04

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf

WORKDIR /home/ctf

COPY main /home/ctf/main
COPY main.c /home/ctf/main.c
COPY flag.txt /home/ctf/flag.txt

RUN chmod +x /home/ctf/main && chmod 444 /home/ctf/flag.txt

USER ctf

EXPOSE 1333

CMD ["socat", "TCP-LISTEN:1333,reuseaddr,fork", "EXEC:/home/ctf/main"]

