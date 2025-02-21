#!/bin/sh

var='latest'
if [ $# -gt 0 ] ; then
  var=$1
fi

echo "docker build -t langfarm/langfarm:${var} ."
docker build -t langfarm/langfarm:${var} .
