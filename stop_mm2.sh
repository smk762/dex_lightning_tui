#!/bin/bash
source rpc
curl --url "http://${rpcip}:${rpcport}" --data "{\"userpass\":\"$userpass\",\"method\":\"stop\"}"