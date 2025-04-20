# Use the official Python 3.10 Alpine image as the base
FROM python:3.12-alpine

# Create a non-root user and switch to it
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set the working directory
WORKDIR /app

# Copy only necessary files
COPY --chown=appuser:appgroup . /app

# Set permissions for the entire /app directory
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Install the dependencies
RUN pip install --no-cache-dir .

# Set the entry point to run the starcloner script
ENTRYPOINT ["python3", "/app/starcloner.py"]
