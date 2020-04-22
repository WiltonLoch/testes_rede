from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
from testes import Testes

def experimento():
    Cleanup.cleanup()
    topo = arvoreMultiNos()
    rede = Mininet(topo = topo, host = CPULimitedHost, link = TCLink)
    rede.start()
    dumpNodeConnections(rede.hosts)
    print("Preparando o ambiente de testes ", end = '')
    #for i in range(0, 9):
    Testes.emitir_sl(rede, carga = '1K', 0, 10)    
    Testes.iperfMultiNos(rede, carga = '250M', comportamento = 'bisection');
    rede.stop()

def main():
    experimento()

if __name__ == '__main__':
    main()
