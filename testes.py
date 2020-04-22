from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.clean import Cleanup
from topologia import arvoreMultiNos
import time

class Testes:
    @staticmethod
    def dividirCarga(carga, qtd_hosts):
        if carga[-1] == "G":
            carga = str(int(carga.strip('G'))*1024) + 'M'
        print(carga)
        carga_numerica = int(carga.strip("KM"))
        carga_numerica = carga_numerica//(qtd_hosts//2);
        return str(carga_numerica) + carga[-1]

    @classmethod
    def iperfMultiNos(cls, rede, carga = '', comportamento = ''):
        hosts = rede.hosts
        qtd_hosts = len(hosts)
        if comportamento == 'bisection':
            if carga:
                carga = '--bitrate ' + cls.dividirCarga(carga, qtd_hosts)
            print(carga)
            for i in range(qtd_hosts//2):
                hosts[(i + qtd_hosts//2)%qtd_hosts].cmd('iperf3 --server > /tmp/h%s_rcv.out &' % ((i + qtd_hosts//2)%qtd_hosts))
                hosts[i].cmd('iperf3 --time 10 ' + carga + ' --client %s --bidir > /tmp/%s_send.out &' % (hosts[(i + qtd_hosts//2)%qtd_hosts].IP(), hosts[i]))

    @staticmethod
    def carregarCPU(rede, carga = 0):
        for h in rede.hosts:
            h.cmd("stress-ng -t 8 -c 1 -l %s &" % carga)

    @staticmethod
    def emitir_sl(rede, carga = '', origem, destino):
            rede.hosts[destino].cmd('(socat -u TCP-LISTEN:5440 stdout | wc -c) >> /tmp/sl_bytes.out &')
            print(rede.hosts[origem].cmd('tail -c ' + carga + ' data | socat -u stdin TCP-CONNECT:%s:5440' % rede.hosts[11].IP()))

#if __name__ == '__main__':
#    main()

#tests = {'teste_sl' : teste_sl}
