#!/bin/bash
cd ..
git clone https://github.com/mininet/mininet.git && cd mininet
git checkout -b 2.3.0d6
./util/install.sh -a
cd ..
sudo apt-get --yes install mininet python3-numpy socat iperf3
wget https://releases.ubuntu.com/20.04/ubuntu-20.04-desktop-amd64.iso?_ga=2.123676172.648246392.1594065166-813380206.1591808348
head -c 1G ubuntu-20.04-desktop-amd64.iso?_ga=2.123676172.648246392.1594065166-813380206.1591808348 | hexdump > testes_rede/data
sudo rm -rf mininet openflow pox
sudo rm ubuntu-20.04-desktop-amd64.iso?_ga=2.123676172.648246392.1594065166-813380206.1591808348
