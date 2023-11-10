# Use the official MongoDB image from Docker Hub
FROM mongo:latest

# Create necessary directories and set permissions
RUN mkdir -p /data/db /data/configdb \
    && chown -R mongodb:mongodb /data/db /data/configdb

# Expose the default MongoDB port
EXPOSE 27017

# Switch to the non-root user when running the container
USER mongodb

# Start MongoDB when the container starts
CMD ["mongod"]

