#!/bin/bash

echo "Container is running!!!"

if [ ! -f /.dockerenv ]; then
    echo "This script needs to run inside the Docker image"
    exit 1
fi

pipenv shell