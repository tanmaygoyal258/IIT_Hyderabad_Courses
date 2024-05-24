#!/bin/sh

sudo tc qdisc add dev h2-eth0 root netem rate 10Mbit limit 100
sudo tc qdisc change dev h2-eth0 root netem delay 150ms
sudo tc qdisc change dev h2-eth0 root netem loss 0.5%
