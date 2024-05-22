# Choose our version of Python
FROM python:3.12

# Set up a working directory
WORKDIR /backend

# Copy just the requirements into the working directory so it gets cached by itself
COPY ./requirements.txt ./requirements.txt

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# Copy the source code into the working directory
COPY ./src/. ./src

EXPOSE 8250

# Run our entry file, which will start the server
CMD ["python", "-m", "src.main", "--host", "0.0.0.0"]
