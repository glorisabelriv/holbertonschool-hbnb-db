# Use an official Python runtime as a parent image
FROM python:3.8-alpine

# Set environment variables
ENV DEVELOPMENT=1

# Install dependencies
RUN apk update && \
	apk add --no-cache postgresql-dev gcc python3-dev musl-dev libffi-dev openssl-dev && \
	rm -rf /var/cache/apk/*

# Set the working directory
WORKDIR /app

# Copy the requirements file first for caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
	pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app

# Expose port 5000 for the application
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
