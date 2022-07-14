# Set base image (host OS)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Create a new user with UID
RUN adduser --disabled-password --gecos '' --system --uid 1001 python && chown -R python /code

# Copy the dependencies file to the working directory
COPY processing_service/requirements.txt .

# Install dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && python3 -m pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY processing_service /processing_service

# Copy file requirements
COPY database.ini .
COPY model /processing_service/model
COPY sources/microchanges.csv .

# Set user to newly created user
USER 1001

# Command to run on container start
CMD [ "python", "/processing_service/main.py" ]
