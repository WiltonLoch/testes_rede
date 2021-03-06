from pathlib import Path
from datetime import timedelta
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

import time
import math
import random

def parseIperf(indice, indice_interno, carga):
    entrada = open("../dados_brutos/%s/%s_" % (indice, indice_interno) + carga, "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo %s/%s_" % (indice, indice_interno) + carga)
        return
    tempos = entrada.read()
    entrada.close()
    tempos = tempos.split('- - - -', 1)[0].splitlines()[-1]
    tempos = tempos.split()[2].split('-')[1]
    return tempos

def parseSocat(indice, indice_interno, carga):
    entrada = open("../dados_brutos/%s/%s_" % (indice, indice_interno) + carga, "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo %s/%s_" % (indice, indice_interno) + carga)
        return
    tempos = entrada.read()
    entrada.close()
    tempos = tempos.rsplit('socket', 1)[0].split('reading', 1)[1].splitlines()
    tempo_inicial, tempo_final = tempos[1], tempos[-1]
    tempo_inicial = [float(x) for x in tempo_inicial.split()[1].split(':')]
    tempo_final = [float(x) for x in tempo_final.split()[1].split(':')]
    tempo_inicial = timedelta(hours = tempo_inicial[0], minutes = tempo_inicial[1], seconds = tempo_inicial[2])
    tempo_final = timedelta(hours = tempo_final[0], minutes = tempo_final[1], seconds = tempo_final[2])
    resultado = tempo_final - tempo_inicial
    return str(resultado).split(':')[2]

def extrairTempos():

    ###################### LEITURA DO ARQUIVO COM OS CASOS DE TESTE #############################

    entrada = open("../config/casos_teste", "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo com os casos de teste")
        return
    arquivos = entrada.read().splitlines()
    entrada.close()
    quantidade_testes = len(arquivos)
    arquivos = [x.split() for x in arquivos]
    curva_x = np.arange(0, quantidade_testes, 1);
    curva_y = []
    tempos = defaultdict(list) 
    for i in range(quantidade_testes):
        curva_y.append(len(arquivos[i]))
        for j in range(len(arquivos[i])):
            carga_atual = arquivos[i][j]
            if(carga_atual[-1] != 'K'):
                tempo_atual = parseIperf(i, j, carga_atual)
            else:
                tempo_atual = parseSocat(i, j, carga_atual)
            tempos[(carga_atual, i)].append(tempo_atual)
    plotarResultados(tempos, curva_x, curva_y)

def plotarResultados(tempos, curva_x, curva_y):
    plt.plot(curva_x, curva_y)
    cargas = ['1K', '10K', '100K', '1M', '10M', '250M', '500M', '1G']
    print(tempos['1G', 21])
    for i in cargas:
        pontos_x, pontos_y = [], []
        for j in curva_x:
            if(tempos[i, j]):
                pontos_x.append(j)
                if(len(tempos[i, j]) > 1):
                    media = 0
                    for k in tempos[i, j]:
                        media += float(k)/len(tempos[i, j])
                    pontos_y.append(media) 
                else:
                    pontos_y.append(float(tempos[i, j][0]))
        # print(i, pontos_x, pontos_y)
        plt.plot(pontos_x, pontos_y, label = i)
    plt.legend()
    plt.show()



    plt.show()


def main():
    extrairTempos()

if __name__ == '__main__':
    main()
