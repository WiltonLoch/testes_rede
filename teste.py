from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
import time

def iperfMultiNos(rede, comportamento = 0):
    hosts = rede.hosts
    qtd_hosts = len(hosts)
    if comportamento == 0:
        for i in range(qtd_hosts):
            hosts[i].cmd('sleep 0.5 && iperf -t 7 -c %s > /tmp/%s_send.out &' % (hosts[(i + qtd_hosts//2)%qtd_hosts].IP(), hosts[i]))
            hosts[(i + qtd_hosts//2)%qtd_hosts].cmd('iperf -s &')

def carregarCPU(rede, carga = 0):
    for h in rede.hosts:
        h.cmd("stress-ng -t 8 -c 1 -l %s &" % carga)

def emitir_ping(rede, comportamento_sl = 0):
    if comportamento_sl == 0:
        print(rede.hosts[0].cmd('ping -c 5 %s' % rede.hosts[11].IP()))

def teste_sl(comp_sl = 0, comp_iperf = 0, cpu = 0):
    Cleanup.cleanup()
    topo = arvoreMultiNos()
    rede = Mininet(topo = topo, host = CPULimitedHost, link = TCLink)
    rede.start()
    dumpNodeConnections(rede.hosts)
    print("Iniciando escrita dos dataplanes com repasse ICMP...")
    rede.pingAll()
    emitir_ping(rede)
    carregarCPU(rede)
    iperfMultiNos(rede)
    time.sleep(3)
    emitir_ping(rede)
    time.sleep(4.5)
    rede.stop()
    
def main():
    teste_latencia()

if __name__ == '__main__':
    main()

tests = {'teste_sl' : teste_sl}
