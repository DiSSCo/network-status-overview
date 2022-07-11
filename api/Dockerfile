# Set base image (host OS)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /api

# Create a new user with UID
RUN adduser --disabled-password --gecos '' --system --uid 1001 python && chown -R python /api

# Copy the dependencies file to the working directory
COPY api/requirements.txt .

# Install dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && python3 -m pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY api /api

# Copy file requirements
COPY database.ini .
COPY model /api/model

# Expose port
EXPOSE 8000

# Set user to newly created user
USER 1001

# Command to run on container start
CMD [ "gunicorn", "main:app", "localhost:8083"]