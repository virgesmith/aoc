#!/bin/bash

if [ "$#" -ne "1" ]; then
  echo "$0 <year>"
  exit 1
fi

year=$1

for day in {1..25}; do
  mkdir -p $year/$day
done