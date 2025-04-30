from ubuntu@sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782 AS app

FROM pwn.red/jail

COPY --from=app / /srv

COPY main /srv/app/run
COPY flag.txt /srv/app/

RUN chmod +x /srv/app/run

RUN rm -f /bin/sh /bin/bash /bin/dash /bin/zsh /usr/bin/sh /usr/bin/bash /usr/bin/dash /usr/bin/zsh /bin/ash /usr/bin/ash

