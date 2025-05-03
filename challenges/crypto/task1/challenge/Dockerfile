# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY syb3lik.py /app/syb3lik.py

# Expose the port the server will listen on
EXPOSE 1337

# Command to run the Python script
CMD ["python", "syb3lik.py"]
