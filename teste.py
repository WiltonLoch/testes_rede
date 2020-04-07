from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
import time

def iperfMultiNos(rede):
    hosts = rede.hosts
    qtd_hosts = len(hosts)
    for i in range(qtd_hosts):
        #print(i, (i + qtd_hosts/2)%qtd_hosts)
        hosts[i].cmd('sleep 0.5 && iperf -t 7 -c %s > /tmp/%s_send.out &' % (hosts[(i + qtd_hosts//2)%qtd_hosts].IP(), hosts[i]))
        hosts[(i + qtd_hosts//2)%qtd_hosts].cmd('iperf -s &')

def carregarCPU(rede):
    for h in rede.hosts:
        h.cmd("stress-ng -t 8 -c 1 -l 50 &")

def teste_latencia():
    Cleanup.cleanup()
    topo = arvoreMultiNos()
    rede = Mininet(topo = topo, host = CPULimitedHost, link = TCLink)
    rede.start()
    dumpNodeConnections(rede.hosts)
    print("Iniciando escrita dos dataplanes com repasse ICMP...")
    rede.pingAll()
    ping_result = rede.hosts[0].cmd('ping -c 5 %s' % rede.hosts[11].IP())
    print(ping_result)
    #CLI(net)
    #time.sleep(6)
    carregarCPU(rede)
    iperfMultiNos(rede)
    time.sleep(3)
    ping_result = rede.hosts[0].cmd('ping -c 5 %s' % rede.hosts[11].IP())
    print(ping_result)
    time.sleep(4.5)
    rede.stop()
    
def main():
    teste_latencia()

if __name__ == '__main__':
    main()
