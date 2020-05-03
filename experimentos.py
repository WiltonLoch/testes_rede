from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
from testes import Testes
from datetime import timedelta
from pathlib import Path

import time

def rajadas_sl(rede, carga, execucoes = 1, intervalo = 0, aquecimento = 0):
    resultados = []
    for i in range(1, execucoes + 1):
        if i == 1 and aquecimento != 0:
            time.sleep(aquecimento)
        elif intervalo:
            time.sleep(intervalo)
        print("Executando teste %s/%s" % (i, execucoes), end = "\r")
        intermediario = Testes.emitir_sl(rede, carga, 0, 10)
        if intermediario < timedelta(microseconds = 100):
            exit()
        #print(intermediario)
        resultados.append(intermediario)
    print("")
    return resultados

def experimento():
    Cleanup.cleanup()
    topo = arvoreMultiNos()
    rede = Mininet(topo = topo, host = CPULimitedHost, link = TCLink)
    rede.start()
    dumpNodeConnections(rede.hosts)

    print("\n===============================")
    print("\nPreparando o ambiente de testes\n")
    print("===============================\n")

    #print("Modificando o controle de congestionamento para DCTCP...")
    #print("Ativando as marcações ECN...")

    #for i in rede.hosts:
    #    i.cmd("sysctl -w net.ipv4.tcp_congestion_control=dctcp; sysctl -w net.ipv4.tcp_ecn=1")

    for i in range(0, 10):
        print("h%s <-> h%s -- " % (i, i + 10), end = "")
        print(Testes.emitir_sl(rede, '1K', i, i + 10))

    print("\n==============================")
    print("\nLendo arquivos de configuração\n")
    print("==============================\n")

    entrada = open("config", "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo de configuração")
        return
    parametros = [x.split()[2:] for x in entrada.read().splitlines()]
    entrada.close()

    execucoes = int(parametros[0][0])
    intervalo = float(parametros[1][0])
    aquecimento = float(parametros[2][0])
    cargas_sl = parametros[3]
    cargas_trafego = parametros[4]
    print(execucoes, intervalo, aquecimento, cargas_sl, cargas_trafego)
    del parametros

    print("\n===================")
    print("\nDisparando SLs base\n")
    print("===================\n")

    Path('resultados/baseline').mkdir(parents = True, exist_ok = True)
    for i in cargas_sl:
        print("carga: " + i)
        saida = open('resultados/baseline/%s' % i, 'w+')
        resultados = rajadas_sl(rede, i, execucoes, intervalo)
        for j in resultados:
            saida.write('%s\n' % str(j).split(':')[2])
        media = sum(resultados, timedelta(0))/len(resultados)
        print("\n", media)
        saida.close()

    print("\n===========================")
    print("\nIniciando adição de tráfego\n")
    print("===========================\n")

    for i in cargas_trafego:
        print("Trafego adicional: " + i)
        Path('resultados/%s' % i).mkdir(parents = True, exist_ok = True)
        for j in cargas_sl:
            print("Carga de teste: " + j)
            saida = open('resultados/%s/%s' % (i, j), 'w+')

            Testes.iperfMultiNos(rede, i, 'bisection', tempo = 1000)
            resultados = rajadas_sl(rede, j, execucoes, intervalo, aquecimento)
            print("Interrompendo iperfs")
            Testes.interromperIperf(rede)

            for k in resultados:
                saida.write('%s\n' % str(k).split(':')[2])

            media = sum(resultados, timedelta(0))/len(resultados)
            print("\n", media)
            print(" --------------- ")
            saida.close()
            time.sleep(5)
    rede.stop()

def main():
    experimento()

if __name__ == '__main__':
    main()
