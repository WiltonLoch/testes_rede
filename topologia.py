from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.link import TCLink

class arvoreMultiNos(Topo):
    "Topologia destinada a criacao de uma arvore tree-tier com quantidade arbitraria de nos e switches"
    def build(self, switches=3, nos=20):
        for i in range(nos):
            #Cria os hosts de acordo com o índice
            host = self.addHost('h%s' % i, cpu=0.8/nos)
            #Cria os switches no mesmo loop já que sw <= nodes
            if(i < switches):
                print(self.addSwitch('s%s' % i))
            #Cria os links de cada host para o sw respectivo (sw0 recebe uma metade e sw1 a outra)
            #Como a topologia inicial possui apenas 3 switches é possível dividir os links da seguinte forma
            sw_dest = i//(nos//(switches - 1))
            #Caso uma árvore mais complexa fosse utilizada esta parte deveria ser modificada
            self.addLink(host, 's%s' % sw_dest, bw=1000);
        self.addLink('s0', 's2')
        self.addLink('s1', 's2')

topos = {'arvoreMultiNos' : arvoreMultiNos}
