FROM python:3.8-slim-buster
RUN apt update -y && apt upgrade -y
RUN /usr/sbin/useradd --no-create-home -u 1000 ctf
WORKDIR /app
COPY ./app .
RUN chown -R ctf:ctf /app
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x start.sh
USER ctf
ENV FLASK_ENV=production
ENTRYPOINT ["/app/start.sh"]