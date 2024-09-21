FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY app/ .

# Expose the application port (adjust if needed)
EXPOSE 8000

# Define the entrypoint for the application
CMD ["fastapi", "run"]