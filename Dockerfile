# Base Image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python output immediately
ENV PYTHONUNBUFFERED=1

# Working Directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy Project
COPY . .

# Expose Flask Port
EXPOSE 5000

# Start Application
CMD ["python", "app.py"]
