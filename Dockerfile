
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements.txt ./requirements.txt
RUN python -m venv /opt/venv
RUN /opt/venv/bin/pip install --upgrade pip setuptools wheel
RUN /opt/venv/bin/pip install -r ./requirements.txt

# Copy the Django project files
COPY . /app

# Install gunicorn
RUN  /opt/venv/bin/pip install gunicorn

# Copy entrypoint script and grant executable permissions
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the application with entrypoint
ENTRYPOINT ["/entrypoint.sh"]
