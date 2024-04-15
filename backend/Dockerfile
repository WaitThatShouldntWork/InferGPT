# Choose our version of Python
FROM python:3.12

# Get args from .env
ARG frontend_url_in_dockerfile=$FRONTEND_URL

# Set up a working directory
WORKDIR /backend_code

# Copy just the requirements into the working directory so it gets cached by itself
COPY requirements.txt /backend_code/requirements.txt

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir --upgrade -r /backend_code/requirements.txt

# Copy the code into the working directory
COPY . /backend_code

EXPOSE 8250

# Tell uvicorn to start spin up our code, which will be running inside the container now
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8250"]
