#!/bin/bash

docker build --no-cache -f Dockerfile_app -t streamflix_app .;
docker build --no-cache -f Dockerfile_server -t streamflix_server .;

#docker build -f Dockerfile_app -t streamflix_app .
#docker build -f Dockerfile_server -t streamflix_server .

docker build -f Dockerfile_nginx -t my_nginx .;

docker-compose up -d --remove-orphans;

docker-compose ps;