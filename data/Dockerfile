# Choose our version of Node
FROM neo4j:5.19.0

# Set up a working directory
WORKDIR /data

# Copy the data content into the working directory
COPY . /data

# Expose port for writing to the database and viewing the graph
EXPOSE 7474
EXPOSE 7687
