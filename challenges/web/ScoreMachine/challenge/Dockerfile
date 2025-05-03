FROM markdown-image

RUN apt update && apt install -y gunicorn3 python3-flask && apt-get install -y adduser

COPY ./app /app/

RUN adduser coinmachine --disabled-password

RUN mkdir -p /opt/core/rscripts
RUN chown coinmachine:coinmachine /opt/core/rscripts/

USER root
COPY ./rscripts /opt/core/rscripts/

WORKDIR /app/

USER coinmachine

CMD gunicorn --workers=16 --threads=16 --bind 0.0.0.0:5000 wsgi:app
