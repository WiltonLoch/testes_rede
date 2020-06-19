from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
from datetime import timedelta
from pathlib import Path
import time
import random

class Testes:
    @staticmethod
    def carregarCPU(rede, carga = 0):
        for h in rede.hosts:
            h.cmd("stress-ng -t 8 -c 1 -l %s &" % carga)

    @staticmethod
    def emitir_sl_paralelos(rede, cargas, caminho, portas_escolhidas, portas_em_uso, alocacoes, politica, matrizPulos):
        for i in range(len(cargas)):
            print(len(cargas))
            escalonamento = politica(rede, alocacoes, matrizPulos)
            origem, destino = escalonamento[0], escalonamento[1]
            if(len(portas_escolhidas) != 0):
                porta = portas_escolhidas[-1] + 1
            else:
                porta = 1024

            while(porta in portas_em_uso + portas_escolhidas):
                porta += 1
            portas_escolhidas.append(porta)
            if(cargas[i][-1] == 'K'):
                comando_servidor = 'socat -u TCP-LISTEN:' + str(porta) + ',reuseaddr FILE:/dev/null'
                comando_cliente = 'sleep 0.5 && tail -c ' + cargas[i] + ' data | socat -lf ' + caminho + '/%s_' % i + cargas[i] + ' -lu -ddd -u stdin TCP-CONNECT:%s:%s' % (rede.hosts[destino].IP(), porta)
            else:
                comando_servidor = 'iperf3 --server -p ' + str(porta) + ' --one-off'
                comando_cliente = 'sleep 0.5 && iperf3 --client %s' % rede.hosts[destino].IP() + ' -p ' + str(porta) + ' --verbose --bytes ' + cargas[i] + ' --logfile ' + caminho + '/%s_' % i + cargas[i]
            #print(comando_servidor, comando_cliente)

            rede.hosts[destino].popen(comando_servidor.split(), shell = True)
            processo = rede.hosts[origem].popen(comando_cliente.split(), shell = True)
            removiveis = []
            for j in alocacoes:
                if j[0][-1] == 'K':
                    removiveis.append(j)
                else:
                    saida_top = [x.split()[0] for x in rede.hosts[j[1]].cmd('top -n 1 -b -p %s' % j[-1]).splitlines()[7:]]
                    if str(j[3]) not in saida_top:
                        removiveis.append(j)

            for j in removiveis:
                alocacoes.remove(j)

            alocacoes.append((cargas[i], origem, destino, processo.pid))
            print(alocacoes)

    @staticmethod
    def emitir_sl(rede, carga, origem, destino):
        rede.hosts[destino].cmd('socat -u TCP-LISTEN:5440,reuseaddr stdout &')
        tempos = rede.hosts[origem].cmd('sleep 0.5 && tail -c ' + carga + ' data | socat -lu -ddd -u stdin TCP-CONNECT:%s:5440' % rede.hosts[destino].IP())
        #print(tempos)
        tempos = tempos.rsplit('socket', 1)[0].split('reading', 1)[1].splitlines()
        tempo_inicial, tempo_final = tempos[1], tempos[-1]
        tempo_inicial = [float(x) for x in tempo_inicial.split()[1].split(':')]
        tempo_final = [float(x) for x in tempo_final.split()[1].split(':')]
        tempo_inicial = timedelta(hours = tempo_inicial[0], minutes = tempo_inicial[1], seconds = tempo_inicial[2])
        tempo_final = timedelta(hours = tempo_final[0], minutes = tempo_final[1], seconds = tempo_final[2])
        return tempo_final - tempo_inicial

#if __name__ == '__main__':
#    main()

#tests = {'teste_sl' : teste_sl}
