# Start with bare ubutnu image
FROM ubuntu:16.04

#changes our directory within ubuntu to /app
WORKDIR /app

# Add coding test files into the app directory
# make sure all coding test files are in the same directory as the Dockerfile, e.g.:
# cp ~/Documents/GitHub/prolegocodingtest/* .

ADD . /app

# Update the image to the latest packages
RUN apt-get update && apt-get upgrade -y

# Install basic unix tools. Add whatever to this.
RUN apt-get install less nano -y

# Install git.
RUN apt-get install git -y

# **Optional** Clone the repository if the Docker image doesn't contain the latest version of the project code
# RUN git clone https://github.com/kevindewalt/prolegocodingtest.git

# packages for coding test
RUN apt-get install sudo postgresql postgresql-contrib libpq-dev python-pip -y
RUN pip install -r requirements.txt

# Create the test database and database user, and grant the user the necessary privileges
RUN sudo -u postgres psql < reset_database.sql

# Set the Flask app environment variables
# **Warning** Do not place actual production/sensitive data and secret keys here or anywhere else in plain text!!!
RUN export DB_USERNAME="prolegotest_user"
RUN export DB_PASSWORD="my_password"
RUN export DB_NAME="prolegotest_db"


#
# Expose port 80
# EXPOSE 80
# Expose port 5000
EXPOSE 5000

#
# Last is the actual command to start up NGINX within our Container
# CMD ["nginx", "-g", "daemon off;"]
