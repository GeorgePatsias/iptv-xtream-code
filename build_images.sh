#!/bin/bash

# Build Images
docker build --no-cache -f Dockerfile_app -t streamflix_app .;
docker build --no-cache -f Dockerfile_server -t streamflix_server .;
docker build -f Dockerfile_nginx -t my_nginx .;

# Start Docker Compose
docker-compose up -d --remove-orphans;
docker-compose ps;

# Initialize Mongo Indexes
# pip install pymongo werkzeug
# python3 init_mongodb.py
