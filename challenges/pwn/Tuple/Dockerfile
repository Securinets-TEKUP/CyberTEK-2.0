FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y python3 netcat && \
    rm -rf /var/lib/apt/lists/*

# Create working directory
RUN useradd -m ctfplayer 
WORKDIR /challenge

# Copy challenge file
COPY ./flag.txt /challenge/flag.txt
COPY ./chal.py /challenge/chal.py

# Make the script executable
RUN chown root:root /challenge/* && \
    chmod 4755 /challenge/chal.py





RUN chown root:root /challenge/flag.txt
RUN chown root:root /challenge/chal.py
RUN  chmod 4755 /challenge/chal.py /challenge/flag.txt 
RUN chmod -w /challenge


RUN chmod 444 /challenge/flag.txt
USER ctfplayer

# Expose the port where the service will listen
EXPOSE 5000

# Start the challenge service using a named pipe approach
CMD ["bash", "-c", "rm -f /tmp/f && mkfifo /tmp/f; cat /tmp/f | python3 /challenge/chal.py | nc -l -p 5000 > /tmp/f"]

