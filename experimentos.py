from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
from testes import Testes
from datetime import timedelta
import time

def rajadas_sl(rede, carga, execucoes = 1, intervalo = 0):
    resultados = []
    for i in range(1, execucoes + 1):
        if intervalo:
            time.sleep(intervalo)
        print("Executando teste %s/%s" % (i, execucoes), end = "\r")
        intermediario = Testes.emitir_sl(rede, carga, 0, 10)
        print(intermediario)
        resultados.append(intermediario)
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
    execucoes = int(parametros[0][0])
    intervalo = float(parametros[1][0])
    cargas_sl = parametros[2]
    cargas_trafego = parametros[3]
    del parametros

    print("\n===================")
    print("\nDisparando SLs base\n")
    print("===================\n")
    for i in cargas_sl:
        resultados = rajadas_sl(rede, i, execucoes, intervalo)
        media = sum(resultados, timedelta(0))/len(resultados)
        print("\n", media)
    print("\n===========================")
    print("\nIniciando adição de tráfego\n")
    print("===========================\n")
    for i in cargas_trafego:
        print("Trafego adicional: " + i)
        for j in cargas_sl:
            print("Carga de teste: " + j)
            Testes.iperfMultiNos(rede, i, 'bisection', tempo = execucoes*intervalo + 3)
            resultados = rajadas_sl(rede, i, execucoes, intervalo)
            media = sum(resultados, timedelta(0))/len(resultados)
            print("\n", media)
            time.sleep(5)
    rede.stop()

def main():
    experimento()

if __name__ == '__main__':
    main()
