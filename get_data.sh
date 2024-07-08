#!/bin/bash

API_URL='https://core.urbansharing.com/public/api/v1/graphql?operationName=DockGroups&variables=%7B%22systemId%22%3A%22oslobysykkel%22%7D&extensions=%7B%22persistedQuery%22%3A%7B%22version%22%3A1%2C%22sha256Hash%22%3A%226afd0a33ab1a81d87dd31830e4e3f3da6f9e0881a9a07427b59bf1dec6fd692e%22%7D%7D'

curl -s "$API_URL" | jq --compact-output --raw-output | gzip > $(dirname "$0")/data/json_$(date +%Y%m%d_%H%M%S).json.gz
