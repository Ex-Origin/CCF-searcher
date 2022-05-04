#!/bin/sh

cd `dirname $0`

rm -f err out
docker run --name rank --rm -d -v`pwd`:/rank -p9031:9031 rank
