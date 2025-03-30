FROM python:3.10-slim

WORKDIR /app

# Copy the entire src directory into the container
COPY src /app/src

# Install dependencies (brotli is needed, gzip is built-in)
RUN pip install brotli

# Set the working directory to src so the script runs correctly
WORKDIR /app/src

# Run the script when the container starts
ENTRYPOINT ["python", "main.py"]