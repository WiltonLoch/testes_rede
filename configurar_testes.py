from datetime import timedelta
from pathlib import Path

import time

def gerarCurvas():

    ###################### LEITURA DAS CURVAS DOS RATOS ##############################

    entrada = open("config/curvas/ratos", "r")
    if entrada.mode != 'r':
        print("Não foi possível abrir o arquivo de curvas dos ratos")
        return
    #quebra o arquivo de entrada por linhas, eliminha os rótulos dos parâmetros e remove itens vazios(linhas com { ou })
    parametros = [i for i in [x.split()[2:] for x in entrada.read().splitlines()] if i]
    tempo_duracao = parametros[0]
    tamanhos_ratos = parametros[1]

    #remove os dois parâmetros já lidos e converte todos os parâmetros das curvas para float
    parametros = [float(i[0]) for i in parametros[2:]]
    #cria uma lista de curvas em que cada item é outra lista contendo os parâmetros
    curvas_ratos = [parametros[i:i+3] for i in range(0, len(parametros), 3)]
    print(curvas_ratos)
    
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
    else:
        for i in curvas_ratos:
            i[2] *= float(copia_ratos[1])
            curvas_elefantes.append(i)
        
    print(curvas_elefantes)

    entrada.close()




def main():
    gerarCurvas()

if __name__ == '__main__':
    main()
