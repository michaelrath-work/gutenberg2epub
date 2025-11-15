#! /bin/env bash

# Fetch the raw data from the source
BASE_URL="https://www.projekt-gutenberg.org/shelley/frankens"

for i in {1..29}
do
  chapter=$(printf "%03d" $i)
  url="$BASE_URL/chap$chapter.html"
  echo "fetch:" $url
  wget $url
done

