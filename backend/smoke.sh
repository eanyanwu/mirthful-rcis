#!/bin/bash

rm ./cookie.txt
# POST /login
curl localhost:5000/login --data "username=eanyanwu&password=password" --cookie-jar ./cookie.txt 

# POST /api/rci 
curl localhost:5000/api/rci --cookie ./cookie.txt --data ""

# GET /api/rci/<rci_id>
curl localhost:5000/api/rci/06974c15-f34b-4cf8-943e-ce86f1d1065e --cookie ./cookie.txt
