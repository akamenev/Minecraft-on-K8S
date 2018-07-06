# Using official python runtime base image
FROM python:3.6-alpine

RUN mkdir -p /root/.kube
WORKDIR /root/.kube
ADD config /root/.kube/config

# Set the application directory
WORKDIR /app

# Install our requirements.txt
ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
ADD . /app

# Define our command to be run when launching the container
CMD ["python", "monitoring.py"]