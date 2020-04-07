#import importlib

#importlib.import_module('topologia')

from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
import time

def rodarIperfMultiNos(rede):
    hosts = rede.hosts
    metade = len(hosts)//2
    for i in range(metade):
        hosts[i].cmd('sleep 0.5 && iperf -t 7 -c %s > /tmp/%s_send.out &' % (hosts[i + metade].IP(), hosts[i]))
        hosts[i + metade].cmd('sleep 0.5 && iperf -t 7 -c %s > /tmp/%s_send.out &' % (hosts[i].IP(), hosts[i + metade]))
        hosts[i].cmd('iperf -s &')
        hosts[i + metade].cmd('iperf -s &')

def carregarCPU(rede):
    for h in rede.hosts:
        h.cmd("stress-ng -t 15 -c 1 -l 50 &")

def teste_latencia():
    Cleanup.cleanup()
    topo = arvoreMultiNos()
    net = Mininet(topo = topo, host = CPULimitedHost, link = TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    print("Iniciando escrita dos dataplanes com repasse ICMP...")
    net.pingAll()
    ping_result = net.hosts[0].cmd('ping -c 5 %s' % net.hosts[11].IP())
    print(ping_result)
    #net.runCpuLimitTest(0.1, 5)
    #CLI(net)
    #time.sleep(6)
    iperfMultiNos(net)
    time.sleep(3)
    ping_result = net.hosts[0].cmd('ping -c 5 %s' % net.hosts[11].IP())
    print(ping_result)
    time.sleep(4.5)
    net.stop()
    
def main():
    teste_latencia()

if __name__ == '__main__':
    main()
