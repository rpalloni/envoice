# Pull base image
FROM node:14.15.4

# set environment variables
ENV CHOKIDAR_USEPOLLING=true

# set container working directory /target/in/container
WORKDIR /usr/src/vue

# copy both 'package.json' and 'package-lock.json' 
COPY package*.json ./

# install and cache app dependencies
RUN npm install
RUN npm install @vue/cli@4.5.0 -g
RUN npm install --save axios bulma bulma-toast js-file-download

# copy the content of the local directory to the working directory
# local directory = Dockerfile folder
COPY ./ ./