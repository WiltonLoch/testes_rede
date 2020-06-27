from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink, TCIntf
from mininet.clean import Cleanup
from mininet.util import custom
from topologia import arvoreMultiNos
from testes import Testes
from collections import defaultdict
from politicasEscalonamento import Politicas

from datetime import timedelta
from pathlib import Path
import math

import time
import subprocess

def construirMatrizPulos(rede):
    matrizPulos = []
    tree_depth = math.ceil(math.log(len(rede.switches), 2))
    sws_last_level = math.pow(2, tree_depth - 1)
    nodes = len(rede.hosts)
    hosts_per_tor = nodes//sws_last_level

    links = rede.topo.links()
    pair_paths = []
    paths = defaultdict(list)
    for i in range(len(rede.hosts)):
        for j in range(i, len(rede.hosts)):
            if i != j:
                node_i = rede.hosts[i] 
                node_j = rede.hosts[j] 
                link_i = [link for link in links if link[0] == str(node_i)]
                link_j = [link for link in links if link[0] == str(node_j)]
                pair_paths.append(link_i[0])
                pair_paths.append(link_j[0])
                while(link_i[0][1] != link_j[0][1]):
                    node_i = link_i[0][1]
                    node_j = link_j[0][1]
                    link_i = [link for link in links if link[0] == node_i]
                    link_j = [link for link in links if link[0] == node_j]
                    pair_paths.insert(len(pair_paths) - len(pair_paths)//2, link_i[0])
                    pair_paths.insert(len(pair_paths)//2 + 1, link_j[0])
                paths[(i, j)] = pair_paths[:]
                pair_paths.clear()
    return paths

def experimento():
    Cleanup.cleanup()
    topo = arvoreMultiNos()
    rede = Mininet(topo = topo, host = CPULimitedHost, intf = custom(TCIntf, enable_ecn = True), link = TCLink)
    rede.start()

    print("\n===============================")
    print("\nPreparando o ambiente de testes\n")
    print("===============================\n")

    print("Modificando o controle de congestionamento para DCTCP...")
    print("Ativando as marcações ECN...")

    for i in rede.hosts:
        i.cmd("sysctl -w net.ipv4.tcp_congestion_control=dctcp; sysctl -w net.ipv4.tcp_ecn=1")

    dumpNodeConnections(rede.hosts);
    for i in range(len(rede.hosts)):
        for j in range(i + 1, len(rede.hosts)):
            print("h%s <-> h%s -- " % (i, j), end = "")
            print(Testes.emitir_sl(rede, '1K', i, j))

    matrizPulos = construirMatrizPulos(rede)
    entrada = open("config/casos_teste", "r") 
    if entrada.mode != 'r':
       print("Nao foi possivel carregar o arquivo contendo os casos de teste")
       return

    casos_teste = entrada.read().splitlines()

    portas_escolhidas = []
    alocacoes = []
    for i in range(len(casos_teste)):
       portas_em_uso, erro = subprocess.Popen(['sudo', 'lsof', '-P', '-i', '-n'], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate() 
       if(not erro):
               portas_em_uso = [int(x.split(':')[1].split()[0].split('-')[0]) for x in str(portas_em_uso).split('\\n')[1:-1]]
       else:
           print("Erro ao obter as portas já utilizadas")
           return
       caminho = 'dados_brutos/%s' % i
       Path(caminho).mkdir(parents = True, exist_ok = True)  
       print("Disparando grupo ", i)
       tempo_inicial = time.time()
       Testes.emitir_sl_paralelos(rede, casos_teste[i].split(), caminho, portas_escolhidas, portas_em_uso, alocacoes, Politicas.menorPuloLivre, matrizPulos)
       print(time.time() - tempo_inicial)
       time.sleep(10 - (time.time() - tempo_inicial))


    dumpNodeConnections(rede.hosts)
    #time.sleep(120)

    rede.stop()

def main():
    experimento()

if __name__ == '__main__':
    main()
