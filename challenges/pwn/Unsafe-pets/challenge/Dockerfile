FROM ubuntu:latest as chroot

RUN apt-get update && apt-get install -y \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN /usr/sbin/useradd --no-create-home -u 2000 user

COPY main /app/run
COPY flag.txt /app/flag.txt

FROM pwn.red/jail

COPY --from=chroot / /srv
ENV JAIL_POW=0 JAIL_PORT=1333

WORKDIR /srv/app
RUN chmod +x run
