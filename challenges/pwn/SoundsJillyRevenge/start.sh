#!/bin/bash

# Apply additional security restrictions
# Make the flag file immutable (can't be deleted even by root)
chattr +i /flag.txt

# Use socat to create a network service
socat TCP-LISTEN:9999,reuseaddr,fork EXEC:/challenge/chip8_payload,pty,stderr,setsid,sigint,sane