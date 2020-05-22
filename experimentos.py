from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink, TCIntf
from mininet.clean import Cleanup
from mininet.util import custom
from topologia import arvoreMultiNos
from testes import Testes

from datetime import timedelta
from pathlib import Path

import time
import subprocess

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

    for i in range(len(rede.hosts)):
        for j in range(i + 1, len(rede.hosts)):
            print("h%s <-> h%s -- " % (i, j), end = "")
            print(Testes.emitir_sl(rede, '1K', i, j))

    entrada = open("config/casos_teste", "r") 
    if entrada.mode != 'r':
       print("Nao foi possivel carregar o arquivo contendo os casos de teste")
       return

    casos_teste = entrada.read().splitlines()

    portas_escolhidas = []
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
       Testes.emitir_sl_paralelos(rede, casos_teste[i].split(), caminho, portas_escolhidas, portas_em_uso)
       time.sleep(1)


    dumpNodeConnections(rede.hosts)
    time.sleep(120)

    rede.stop()

def main():
    experimento()

if __name__ == '__main__':
    main()
