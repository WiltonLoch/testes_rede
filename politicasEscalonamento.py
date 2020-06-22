
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
import numpy as np

import time
import random

class Politicas:
    @staticmethod
    def aleatoria(rede, alocacoes, matrizPulos):
        origem = random.randrange(len(rede.hosts))
        destino = random.randrange(len(rede.hosts))
        while(destino == origem):
            destino = random.randrange(len(rede.hosts))
        return (origem, destino)

    @staticmethod
    def menorPuloLivre(rede, alocacoes, matrizPulos):
          print(rede.topo.links())  
