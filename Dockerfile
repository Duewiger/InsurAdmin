# Pull base image
FROM python:3.11.7-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 0
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /InsurAdmin

# Install dependencies
RUN pip install --upgrade pip
RUN pip cache purge
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Install gunicorn
RUN pip install gunicorn

# Copy project
COPY . .