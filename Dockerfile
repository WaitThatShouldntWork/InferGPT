# Use an official Python runtime as a parent image
FROM python:3.11.3-slim

# Install system dependencies required for compiling certain Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade -r requirements.txt

# Copy bot.py and other necessary files or directories into the container
COPY bot.py .

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable to prevent Python from writing pyc files to disc (optional)
ENV PYTHONDONTWRITEBYTECODE 1

# Define environment variable to keep Python from buffering stdout and stderr (optional)
ENV PYTHONUNBUFFERED 1

# Run the application when the container launches
ENTRYPOINT ["streamlit", "run", "bot.py"]
 