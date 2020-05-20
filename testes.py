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
    def emitir_sl_paralelos(rede, cargas, caminho, portas_escolhidas, portas_em_uso):
        for i in range(len(cargas)):
            origem = random.randrange(len(rede.hosts))
            destino = random.randrange(len(rede.hosts))
            while(destino == origem):
                destino = random.randrange(len(rede.hosts))

            if(len(portas_escolhidas) != 0):
                porta = portas_escolhidas[-1] + 1
            else:
                porta = 1024

            while(porta in portas_em_uso + portas_escolhidas):
                porta += 1
            portas_escolhidas.append(porta)
            comando_servidor = 'socat -u TCP-LISTEN:' + str(porta) + ',reuseaddr stdout &'
            comando_cliente = 'sleep 0.5 && tail -c ' + cargas[i] + ' data | socat -lf ' + caminho + '/%s_' % i + cargas[i] + ' -lu -dddd -u stdin TCP-CONNECT:%s:%s' % (rede.hosts[destino].IP(), porta) + ' &'

            rede.hosts[destino].cmd(comando_servidor)
            rede.hosts[origem].cmd(comando_cliente)

    @staticmethod
    def emitir_sl(rede, carga, origem, destino):
        rede.hosts[destino].cmd('socat -u TCP-LISTEN:5440,reuseaddr stdout &')
        tempos = rede.hosts[origem].cmd('sleep 0.5 && tail -c ' + carga + ' data | socat -lu -ddd -u stdin TCP-CONNECT:%s:5440' % rede.hosts[destino].IP())
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
