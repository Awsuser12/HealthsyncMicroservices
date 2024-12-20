# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app/ /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the service (optional if this is a cron-like job)
EXPOSE 5003

# Start the aggregator job
CMD ["python", "main.py"]
