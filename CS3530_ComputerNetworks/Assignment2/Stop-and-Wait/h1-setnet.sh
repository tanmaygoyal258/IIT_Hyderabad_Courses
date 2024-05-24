#!/bin/sh

sudo tc qdisc add dev h1-eth0 root netem rate 10Mbit limit 100
sudo tc qdisc change dev h1-eth0 root netem delay 5ms
sudo tc qdisc change dev h1-eth0 root netem loss 5%
