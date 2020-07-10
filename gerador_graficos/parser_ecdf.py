from pathlib import Path
from datetime import timedelta
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt

import time
import math
import random

import sys
sys.path.append("/files/testes_rede")
from BatchProcess import BatchProcessing

def parseIperf(folder, indice, indice_interno, carga):
    entrada = open("../resultados/" + folder + "/%s/%s_" % (indice, indice_interno) + carga, "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo resultados/" + folder + "%s/%s_" % (indice, indice_interno) + carga)
        return
    tempos = entrada.read()
    entrada.close()
    tempos = tempos.split('- - - -', 1)[0].splitlines()[-1]
    tempos = tempos.split()[2].split('-')[1]
    return tempos

def parseSocat(folder, indice, indice_interno, carga):
    entrada = open("../resultados/" + folder + "/%s/%s_" % (indice, indice_interno) + carga, "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo resultados/" + folder + "%s/%s_" % (indice, indice_interno) + carga)
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

    cargas = ['1K', '10K', '100K', '1M', '10M', '100M']
    queue_ordering = ['fcfs', 'sjf', 'ljf']
    scheduling = ['random', 'netaware']

    test_cases = entrada.read().splitlines()
    entrada.close()
    
    test_cases = [x.split() for x in test_cases]
    test_quantity = len(test_cases)
    tempos = defaultdict(list) 
    for queue_policy in queue_ordering:
        for discipline in scheduling:
            folder = discipline + '_' + queue_policy
            for batch in range(test_quantity):
                if queue_policy == 'sjf':
                    BatchProcessing.sjf(test_cases[batch])
                if queue_policy == 'ljf':
                    BatchProcessing.ljf(test_cases[batch])
                for flow_index in range(len(test_cases[batch])):
                    flow = test_cases[batch][flow_index]
                    if flow[-1] != 'K':
                        result_time = parseIperf(folder, batch, flow_index, flow)
                    else:
                        result_time = parseSocat(folder, batch, flow_index, flow)
                    tempos[(flow, folder)].append(float(result_time))
    for flow_size in cargas:
        plotLoadResults(tempos, flow_size)

def plotLoadResults(times, flow_size):
    queue_ordering = ['fcfs', 'sjf', 'ljf']
    scheduling = ['random', 'netaware']
    y_points = [] 
    for discipline in scheduling:
        for queue_policy in queue_ordering:
            folder = discipline + '_' + queue_policy
            plt.plot(np.sort(times[flow_size, folder]), np.arange(1, len(times[flow_size, folder]) + 1)/len(times[flow_size, folder]), label = folder)
    plt.title("CDF of FCT - " + flow_size + "B flow size")
    plt.xlabel("Time(s)")
    plt.ylabel("CDF")
    plt.legend()
    plt.savefig(flow_size + '.png') 
    plt.clf()

def plotarResultados(tempos, curva_x, curva_y):
    # plt.plot(curva_x, curva_y)
    for i in cargas:
        pontos_y = [] 
        for j in curva_x:
            if(tempos[i, j]):
                for k in tempos[i, j]:
                    pontos_y.append(float(k))
        plt.plot(np.sort(pontos_y), np.arange(1, len(pontos_y) + 1)/len(pontos_y), label = i)
        if i == '100K':
            plt.title("CDF of FCT - Network-aware Scheduling with SJF")
            plt.xlabel("Time(s)")
            plt.ylabel("CDF")
            plt.legend()
            plt.savefig('ecdf_leves.png') 
            plt.clf()
    plt.title("CDF of FCT - Network-aware Scheduling with SJF")
    plt.xlabel("Time(s)")
    plt.ylabel("CDF")
    plt.legend()
    plt.savefig('ecdf_pesadas.png') 

def main():
    extrairTempos()

if __name__ == '__main__':
    main()
