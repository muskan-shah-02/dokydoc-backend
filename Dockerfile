# Start from an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the application code into the container
COPY ./app /app/app
COPY ./main.py /app/main.py

# Expose the port the app runs on
EXPOSE 8000

# The command to run the application will be provided by docker-compose
