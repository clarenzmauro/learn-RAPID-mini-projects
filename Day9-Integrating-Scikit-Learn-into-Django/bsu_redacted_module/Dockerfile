# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to prevent Python from writing .pyc files to disc
# and to prevent Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies (if any are needed later, add them here)
# For example, for PostgreSQL client:
# RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size by not storing the pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code from your local machine
# to /usr/src/app in the container
COPY . .

# Copy the ML models into the image
COPY ./ml_models /usr/src/app/ml_models

# Inform Docker that the container listens on port 8000 at runtime
# This is documentation; actual port publishing happens with 'docker run -p'
EXPOSE 8000

# The command to run when the container starts.
# This will start the Django development server.
# "0.0.0.0" makes the server accessible from outside the container (on the Docker network).
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
