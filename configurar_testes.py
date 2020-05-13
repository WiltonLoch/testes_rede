from pathlib import Path

import time
import math
import random

def aplicarEmCurva(x, curva):
        y = (1/curva[1] * math.sqrt(2 * math.pi))
        y *= math.exp((-1/2) * math.pow((x - curva[0])/curva[1], 2))
        return y

def gerarCurvas():

    ###################### LEITURA DAS CURVAS DOS RATOS ##############################

    entrada = open("config/curvas/ratos", "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo de curvas dos ratos")
        return
    #quebra o arquivo de entrada por linhas, eliminha os rótulos dos parâmetros e remove itens vazios(linhas com { ou })
    parametros = [i for i in [x.split()[2:] for x in entrada.read().splitlines()] if i]
    tempo_duracao = int(parametros[0][0])
    tamanhos_ratos = parametros[1]

    #remove os dois parâmetros já lidos e converte todos os parâmetros das curvas para float
    parametros = [float(i[0]) for i in parametros[2:]]
    #cria uma lista de curvas em que cada item é outra lista contendo os parâmetros
    curvas_ratos = [parametros[i:i+3] for i in range(0, len(parametros), 3)]
    
    ###################### LEITURA DAS CURVAS DOS ELEFANTES ##############################

    entrada = open("config/curvas/elefantes", "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo de curvas dos elefantes")
        return
    parametros = [i for i in [x.split()[2:] for x in entrada.read().splitlines()] if i]
    tamanhos_elefantes = parametros[0]
    copia_ratos = parametros[1]
    curvas_elefantes = []
    #avalia o parâmetro de cópia, se este for 'SIM' então as curvas dos elefantes serão iguais às dos ratos, porém ponderadas por um multiplicador alpha < 1. Caso contrário, lê as curvas próprias dos elefantes contidas no arquivo de configuração respectivo.
    if(copia_ratos[0] == 'NAO'):
        #remove os dois parâmetros já lidos e converte todos os parâmetros das curvas para float
        parametros = [float(i[0]) for i in parametros[2:]]
        #cria uma lista de curvas em que cada item é outra lista contendo os parâmetros
        curvas_elefantes = [parametros[i:i+3] for i in range(0, len(parametros), 3)]
               
    saida = open("config/casos_teste", "w+")
    if saida.mode != 'w+':
        print("Nao foi possível criar o arquivo de saida para os casos de teste")
        return

    random.seed()
    #percorre todos os valores de x de forma crescente
    for x in range(0, tempo_duracao):
        saida.write("%s" % x)
        #define uma variavel para o y tanto dos ratos quanto dos elefantes para aquele x
        y_ratos = 0
        y_elefantes = 0
        #aplica o x em questão em todas as curvas dos ratos e toma o maior valor normalizado em relaçao a quantidade de testes entre o y da curva anterior e a atual
        for i in curvas_ratos:
            y_ratos = round(max(y_ratos, (aplicarEmCurva(x, i)/aplicarEmCurva(i[0], i)) * i[2]))

        #se a copia dos ratos está ativada, apenas gera o y dos elefantes em função dos ratos, dada a porcentagem
        if copia_ratos[0] == 'SIM':
            y_elefantes = round(y_ratos * float(copia_ratos[1]))
        #caso contrário gera o y para os elefantes da mesma forma que para os ratos
        else:
            for i in curvas_elefantes:
                y_elefantes = round(max(y_elefantes, (aplicarEmCurva(x, i)/aplicarEmCurva(i[0], i)) * i[2]))

        #Como a quantidade de ratos é supostamente sempre maior que a quantidade de elefantes, utiliza o mesmo for para escrita de ambos na saída
        for i in range(y_ratos):
            saida.write(" %s" % tamanhos_ratos[random.randrange(len(tamanhos_ratos))])
            if(i < y_elefantes):
                saida.write(" %s" % tamanhos_elefantes[random.randrange(len(tamanhos_elefantes))])
        saida.write("\n")

    entrada.close()




def main():
    gerarCurvas()

if __name__ == '__main__':
    main()
