FROM python:3.11-slim

RUN apt-get update && apt-get install -y socat
RUN pip install pycryptodome
RUN pip install fastecdsa
RUN rm -rf /var/lib/apt/lists/*

WORKDIR .

COPY flipper-zer0.py .

EXPOSE 4871

CMD ["socat", "TCP-LISTEN:4871,fork,reuseaddr", "EXEC:'python3 flipper-zer0.py',stderr"]