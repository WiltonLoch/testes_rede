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

class Testes:
    @staticmethod
    def dividirCarga(carga, qtd_hosts):
        if carga[-1] == "G":
            carga = str(int(carga.strip('G'))*1024) + 'M'
        carga_numerica = int(carga.strip("KM"))
        carga_numerica = carga_numerica//(qtd_hosts//2);
        return str(carga_numerica) + carga[-1]

    @classmethod
    def iperfMultiNos(cls, rede, carga, comportamento, tempo = 10, controle_congest = "dctcp"):
        hosts = rede.hosts
        qtd_hosts = len(hosts)
        flags = '--time %s --congestion %s' % (tempo, controle_congest)
        if comportamento == 'bisection':
            if carga:
                caminho_saida = 'transfs_iperf/' + carga
                Path(caminho_saida).mkdir(parents = True, exist_ok = True)
                carga = '--bitrate ' + cls.dividirCarga(carga, qtd_hosts)
                print(carga)
            for i in range(qtd_hosts//2):
                hosts[(i + qtd_hosts//2)%qtd_hosts].cmd('iperf3 --server >> ' + caminho_saida + '/h%s_rcv.out &' % ((i + qtd_hosts//2)%qtd_hosts))
                hosts[i].cmd('iperf3 ' + carga + ' --client %s --bidir ' % hosts[(i + qtd_hosts//2)%qtd_hosts].IP() + flags + ' >> ' + caminho_saida + '/%s_send.out &' % hosts[i])

    @staticmethod
    def interromperIperf(rede):
        hosts = rede.hosts
        for i in range(0, len(hosts)):
            hosts[i].cmd('pkill iperf3')

    @staticmethod
    def carregarCPU(rede, carga = 0):
        for h in rede.hosts:
            h.cmd("stress-ng -t 8 -c 1 -l %s &" % carga)

    @staticmethod
    def emitir_sl(rede, carga, origem, destino, bloqueante = True, saida = ''):
            rede.hosts[destino].cmd('(socat -u TCP-LISTEN:5440,reuseaddr stdout | wc -c) &')
            comando_cliente = 'sleep 0.3 && tail -c ' + carga + ' data | socat -lu -ddd -u stdin TCP-CONNECT:%s:5440' % rede.hosts[destino].IP()
            if(not bloqueante):
                if(saida):
                    Path('dados_brutos/').mkdir(parents = True, exist_ok = True)
                    comando_cliente += ' & ' + ' >> dados_brutos/' + saida
                else:
                    print("Erro: Chamadas SL não bloqueantes precisam de um arquivo de saída")
                    exit()
            tempos = rede.hosts[origem].cmd(comando_cliente)
            if(bloqueante):
                print(tempos)
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
