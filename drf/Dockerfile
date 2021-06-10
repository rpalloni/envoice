# pull base image
FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set the working directory in the container
WORKDIR /usr/src/drf

# Install wkhtmltopdf https://wkhtmltopdf.org/
RUN apt-get update && \
    apt-get -yq update && \
    apt-get install -y xvfb && \
    apt-get install -y xvfb xfonts-encodings xfonts-utils xfonts-base xfonts-75dpi && \
    apt-get install -y wkhtmltopdf

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local directory to the working directory
# local directory = Dockerfile folder
COPY ./ ./