
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
        retorno = (matrizPulos[0][1], matrizPulos[0][2])  
        rejeitados_associativo = []
        if not alocacoes:
            return retorno
        for i in matrizPulos:
            utilizado = False
            for j in alocacoes:
                if i[1] == j[1] or i[2] == j[2]:
                    utilizado = True
                    break
                elif i[1] == j[2] or i[2] == j[1]:
                    utilizado = True
                    rejeitados_associativo.append((i[1], i[2]))
                    break
            if utilizado == False:
                return (i[1], i[2])

