# Base image
FROM python:3.10

# Update system
RUN apt update -y
RUN apt upgrade -y
RUN pip install -U pip

# Create and use project directory
WORKDIR /app

# Copy and install project requirements
ADD requirements.txt .
RUN pip install -r requirements.txt

# Copy project source files
ADD src .

# Entrypoint
ENTRYPOINT python worker.py
