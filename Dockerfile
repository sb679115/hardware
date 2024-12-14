# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files from the app directory into the Docker container
COPY app/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the application port
EXPOSE 5000

# Run the application
CMD ["python", "/app/app.py"]
