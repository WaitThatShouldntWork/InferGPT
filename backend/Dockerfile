# Choose our version of Python
FROM python:3.12

# Set up a working directory
WORKDIR /backend

# Copy just the requirements into the working directory so it gets cached by itself
COPY ./requirements.txt ./requirements.txt

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# Copy the source code into the working directory
COPY ./src/. /backend/src

EXPOSE 8250

# Tell uvicorn to start spin up our code, which will be running inside the container now
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8250"]
