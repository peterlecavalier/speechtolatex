# Use the official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask API code to the working directory
COPY ttl-api.py .

# Run the Flask API when the container starts
CMD ["python", "ttl-api.py"]