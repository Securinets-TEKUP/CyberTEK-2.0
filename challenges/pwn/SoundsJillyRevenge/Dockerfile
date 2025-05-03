FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    gcc \
    libc6-dev \
    netcat-openbsd \
    socat \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/*

# Create challenge user without password
RUN useradd -m ctfplayer -s /bin/bash

# Create working directory
WORKDIR /challenge

# Copy the source code and files
COPY player.c /challenge/
COPY test /challenge/
COPY chip8 /challenge/
COPY start.sh /challenge/

# Compile the payload binary
RUN gcc -Wall -o /challenge/chip8_payload /challenge/player.c

# Set permissions:
#   - chip8, chip8_payload: setuid root, executable by ctfplayer
#   - start.sh, test: executable by ctfplayer
RUN chown root:root /challenge/chip8 /challenge/chip8_payload && \
    chmod 4755 /challenge/chip8 /challenge/chip8_payload && \
    chown root:root /challenge/start.sh /challenge/test && \
    chmod 755 /challenge/start.sh /challenge/test

# Create a flag file, readable only by root
COPY flag.txt /challenge/
RUN chmod 444 /challenge/flag.txt && \
    chown root:root /challenge/flag.txt


# Expose the port
EXPOSE 9999

# Switch to ctfplayer user
USER ctfplayer

# Command to run when container starts (as ctfplayer)
CMD ["/challenge/start.sh"]
