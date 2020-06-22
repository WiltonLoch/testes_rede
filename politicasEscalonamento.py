
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
import numpy as np

import time
import random

class Politicas:
    @staticmethod
    def aleatoria(rede, carga, alocacoes, matrizPulos):
        origem = random.randrange(len(rede.hosts))
        destino = random.randrange(len(rede.hosts))
        while(destino == origem):
            destino = random.randrange(len(rede.hosts))
        return (origem, destino)

    @staticmethod
    def menorPuloLivre(rede, carga, alocacoes, matrizPulos):
        link_loads = {}
        link_capacity = 1000 * 1000 * 1000
        for i in alocacoes:
            keys = matrizPulos[(i[1], i[2])]
            multiplier = 1000
            if i[-1] == 'M':
                multiplier *= 1000
            elif i[-1] == 'G':
                multiplier *= 1000 * 1000
            for j in keys:
                if not (j[0] + j[1] in link_loads):
                    link_loads[j[0] + j[1]] = (int(i[0][:-1]) * multiplier)/link_capacity
                else:
                    link_loads[j[0] + j[1]] += (int(i[0][:-1]) * multiplier)/link_capacity

        multiplier = 1000
        if carga[-1] == 'M':
            multiplier *= 1000
        elif carga[-1] == 'G':
            multiplier *= 1000 * 1000
        schedule_load = (int(carga[:-1]) * multiplier)/link_capacity

        smallest_load = 1000000
        best_choice = (0, 1)
        for i in range(len(rede.hosts)):
            for j in range(i, len(rede.hosts)):
                if i != j:
                    keys = matrizPulos[(i, j)]
                    choice_additional_load = 0
                    for k in keys:
                        if k[0] + k[1] in link_loads:
                            link_new_load = link_loads[k[0] + k[1]] + schedule_load
                            choice_additional_load += link_new_load/(1 - link_new_load)
                        else:
                            choice_additional_load += schedule_load/(1 - schedule_load)
                    if choice_additional_load < smallest_load:
                        smallest_load = choice_additional_load
                        best_choice = (i, j)
        return best_choice