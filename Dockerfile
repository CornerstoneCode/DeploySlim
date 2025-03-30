# Use an official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the entire repository (including the 'src' folder) into the container
COPY . /app

# Install the required Python packages (brotli)
RUN pip install --no-cache-dir brotli

# If you have other dependencies, install them as well
# RUN pip install -r requirements.txt # Uncomment if you have a requirements.txt file

# Set environment variable for Python to prevent buffer issues in logs
ENV PYTHONUNBUFFERED 1

# Run the Python script when the container is started
ENTRYPOINT ["python", "src/main.py"]
