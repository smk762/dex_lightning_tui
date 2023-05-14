#!/bin/bash
source rpc

nohup ./mm2 > mm2.log &
sleep 3
curl --url "http://${rpcip}:${rpcport}" --data "{\"method\":\"version\",\"userpass\":\"$userpass\"}"
