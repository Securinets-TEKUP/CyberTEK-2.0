FROM ubuntu:22.04

# Set up non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libc6-dev \
    libpthread-stubs0-dev \
    netcat \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user to run the server
RUN useradd -m ctf

# Create challenge directory
WORKDIR /home/ctf/challenge

# Copy source code
COPY mutex_server.c .

# Create flag file
COPY flag.txt . 
RUN  chmod 400 flag.txt && \
    chown ctf:ctf flag.txt

# Compile the challenge
RUN gcc -o mutex_server mutex_server.c -pthread -Wall

# Set permissions
RUN chown -R ctf:ctf /home/ctf/challenge && \
    chmod 550 mutex_server

# Expose the port the server runs on
EXPOSE 6002

# Switch to the non-root user
USER ctf

# Run the server on container start
CMD ["./mutex_server"]
