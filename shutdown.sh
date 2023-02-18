#!/bin/sh
for proc in $(find -name "*.proc"); do kill $(cat $proc); done
