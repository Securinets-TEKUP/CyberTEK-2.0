FROM python:3.11-slim

RUN apt-get update && apt-get install -y socat
RUN pip install cryptography
RUN rm -rf /var/lib/apt/lists/*

WORKDIR .

COPY xtasy.py .

EXPOSE 4869

CMD ["socat", "TCP-LISTEN:4869,fork,reuseaddr", "EXEC:'python3 xtasy.py',stderr"]