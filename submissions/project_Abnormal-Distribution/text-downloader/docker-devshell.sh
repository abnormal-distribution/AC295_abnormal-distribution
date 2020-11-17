#!/bin/bash

set -e

docker build -t text-downloader -f Dockerfile .
docker run --rm --name text-downloader -ti -v "$(pwd)/:/app/" text-downloader