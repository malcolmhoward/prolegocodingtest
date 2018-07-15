# Start with bare ubutnu image
FROM ubuntu:16.04

#changes our directory within ubuntu to /app
WORKDIR /app

# Add coding test files into the app directory
# make sure all coding test files are in the same director as the Dockerfile, e.g.:
# cp ~/Documents/GitHub/prolegocodingtest/* .

ADD . /app

# Update the image to the latest packages
RUN apt-get update && apt-get upgrade -y

# Install basic unix tools. Add whatever to this.
RUN apt-get install less nano -y

# packages for coding test
RUN apt-get install sudo postgresql postgresql-contrib libpq-dev python-pip -y
RUN pip install -r requirements.txt

## Stopped at the point of installing the db.

#
# Expose port 80
# EXPOSE 80

#
# Last is the actual command to start up NGINX within our Container
# CMD ["nginx", "-g", "daemon off;"]
