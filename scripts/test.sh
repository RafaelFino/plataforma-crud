#!/bin/bash
curl 127.0.0.1:5000/products -X POST -H 'Content-Type: application/json' -d '{"name":"Meu produto","desc":"O produto mais lindo que vc ja viu", "price": 33.3}' | jq
curl 127.0.0.1:5000/products -X POST -H 'Content-Type: application/json' -d '{"name":"Meu produto","desc":"O produto mais lindo que vc ja viu", "price": 44.4}' | jq
curl 127.0.0.1:5000/products/1 -X GET -H 'Content-Type: application/json'  | jq
curl 127.0.0.1:5000/products -X GET -H 'Content-Type: application/json' | jq