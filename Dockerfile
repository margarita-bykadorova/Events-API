# Use python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in docker container
WORKDIR /app

# copy requirements.txt
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]

