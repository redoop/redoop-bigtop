#!/bin/bash

docker_image=$1
cmd=$2
docker run --rm -v `pwd`:/ws -v /data/maven/m2:/root/.m2 --workdir /ws ${docker_image} bash -l -c "./gradlew ${cmd}"

