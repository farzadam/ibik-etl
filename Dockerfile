# Dockerfile for running the ETL pipeline

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the ETL pipeline
CMD ["python", "main.py"]
