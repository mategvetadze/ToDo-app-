# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Start the Flask app with Gunicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]