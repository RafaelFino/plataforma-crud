#!/bin/bash
curl 127.0.0.1:5000/products -X GET -H 'Content-Type: application/json' | jq