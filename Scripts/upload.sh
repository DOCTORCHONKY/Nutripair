#!/bin/bash

for num in {1..48} 
do
curl -XPOST -u 'CREDENTIALS' 'ENDPOINT_URL' --data-binary @Nutrient_Values-$num.json -H 'Content-Type: application/json'
done