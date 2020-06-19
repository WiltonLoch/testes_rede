from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.link import TCLink
import math

class arvoreMultiNos(Topo):
    "Topologia destinada a criacao de uma arvore binária completa com profundidade arbitraria"
    def build(self, tree_levels = 3, hosts_per_tor = 5):
        switches = int(math.pow(2, tree_levels) - 1)
        sws_ultimo_nivel = int(pow(2, tree_levels - 1))
        nodes = sws_ultimo_nivel * hosts_per_tor
        for i in range(nodes):
            #Cria os hosts de acordo com o índice
            host = self.addHost('h%s' % i, cpu=0.8/nodes)
            #Cria os switches no mesmo loop já que sw <= nodes
            if(i < switches):
                self.addSwitch('s%s' % i)
            #Cria os links de cada host para o sw respectivo (sw0-3 recebem 5 hosts cada)
            #Como a topologia inicial possui apenas 3 switches é possível dividir os links da seguinte forma
            #O log define a altura da árvore, o ^2 a quantidade de nós no último nível. Divide-se a quantidade de hosts pela quantidade de nós no último nível para se descobrir a quantidade de hosts por nó. Por fim, divisão inteira do índice pelo tamanho do intervalo.
            sw_dest = i//(nodes//sws_ultimo_nivel)
            #Caso uma árvore mais complexa fosse utilizada esta parte deveria ser modificada
            self.addLink(host, 's%s' % sw_dest, delay = '1ms', bw = 1000);

        sw_dest = sws_ultimo_nivel - 1
        #switches - 1 pois o último sw não cria link com nenhum outro 
        for i in range(switches - 1):
            if(i % 2 == 0):
                sw_dest += 1
            self.addLink('s%s' % str(i), 's%s' % sw_dest, delay = '1ms', bw = 1000)

topos = {'arvoreMultiNos' : arvoreMultiNos}
