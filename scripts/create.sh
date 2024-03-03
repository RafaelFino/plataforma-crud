#!/bin/bash
curl 127.0.0.1:5000/products -X POST -H 'Content-Type: application/json' -d '{"name":"Meu produto","desc":"O produto mais lindo que vc ja viu", "price": 33.3}'