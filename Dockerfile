# Set base image (host OS)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Set csv_files directory as mounting volume
#RUN mkdir -p /code/csv_files

# Create a new user with UID
RUN adduser --disabled-password --gecos '' --system --uid 1001 python && chown -R python /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Adding file permission for csv files
RUN chown -R 1001:1001 /code

# Set user to newly created user
USER 1001

# Command to run on container start
CMD [ "python", "main.py" ]
