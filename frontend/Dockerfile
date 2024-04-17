# Choose our version of Node
FROM node:alpine

# Set up a working directory
WORKDIR /app

# Copy just the requirements into the working directory so it gets cached by itself
COPY . /app

# Install the dependencies
RUN npm install

# Expose port app runs on
EXPOSE 8650

# Run app
ENTRYPOINT [ "npm", "start" ]
