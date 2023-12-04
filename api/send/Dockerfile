# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /send

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

ADD morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json /root/morning-nooz-firebase-adminsdk-23o8s-47a5cd78d0.json

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Install Cron
RUN apt-get update && apt-get -y install cron

# Copy the current directory contents into the container at /send
COPY . /send

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the command on container startup
RUN crontab crontab
CMD cron && tail -f /var/log/cron.log
