FROM python:3.11-slim

RUN apt-get update && apt-get install -y socat
RUN pip install cryptography
RUN rm -rf /var/lib/apt/lists/*

WORKDIR .

COPY xtasyyy.py .

EXPOSE 4870

CMD ["socat", "TCP-LISTEN:4870,fork,reuseaddr", "EXEC:'python3 xtasyyy.py',stderr"]