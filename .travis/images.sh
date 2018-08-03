#!/bin/bash

images=$(cat << 'IMAGES'
centos-molecule:7
debian-molecule:8
debian-molecule:9
fedora-molecule:27
ubuntu-molecule:16.04
ubuntu-molecule:18.04
IMAGES
)
for i in ${images} ; do
  docker pull paulfantom/$i &
done

wait
