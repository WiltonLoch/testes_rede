from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
from datetime import timedelta
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
    def iperfMultiNos(cls, rede, carga, comportamento, tempo = 10):
        hosts = rede.hosts
        qtd_hosts = len(hosts)
        flags = '--time %s' % tempo
        if comportamento == 'bisection':
            if carga:
                carga = '--bitrate ' + cls.dividirCarga(carga, qtd_hosts)
            for i in range(qtd_hosts//2):
                hosts[(i + qtd_hosts//2)%qtd_hosts].cmd('iperf3 --server > /tmp/h%s_rcv.out &' % ((i + qtd_hosts//2)%qtd_hosts))
                hosts[i].cmd('iperf3 ' + carga + ' --client %s --bidir ' % hosts[(i + qtd_hosts//2)%qtd_hosts].IP() + flags + ' > /tmp/%s_send.out &' % hosts[i])

    @staticmethod
    def carregarCPU(rede, carga = 0):
        for h in rede.hosts:
            h.cmd("stress-ng -t 8 -c 1 -l %s &" % carga)


    @staticmethod
    def emitir_sl(rede, carga, origem, destino):
            rede.hosts[destino].cmd('(socat -u TCP-LISTEN:5440 stdout | wc -c) >> /tmp/sl_bytes.out &')
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
