# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

#Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app.py file to the workdir
COPY sst-api.py .

# Define environment variable
ENV MODEL="openai/whisper-tiny.en"

# Run app.py when the container launches
CMD ["python", "sst-api.py"]
