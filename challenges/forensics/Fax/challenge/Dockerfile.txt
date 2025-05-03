FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 socat

WORKDIR /app

RUN useradd -m ctf

COPY quiz_server_nc.py ./

RUN chmod +x quiz_server_nc.py

USER ctf

EXPOSE 11002

CMD ["socat", "TCP-LISTEN:11002,reuseaddr,fork", "EXEC:/app/quiz_server_nc.py"]
