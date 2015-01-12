from util import loadFile, loadFilesFromList, loadFilesUntil
from util import getActionRepresentation, getStateRepresentation
import util
import math
import random
import cPickle



input_teste = [  [ [0,0],[0] ] ,[ [1,0],[1] ], [ [0,1],[1] ] , [ [1,1],[1] ] ]

#entradas
numeroEntradas = 3
numeroNeuroniosEscondidos = 2
numeroNeuroniosSaida = 1

#pesos
pesosEntrada = []
pesosSaida = []

#valores iniciais dos pesos
valorBaixo = -0.5
valorAlto = 0.5
    
#activacoes, saidas dos neuronios
activacoesCamadaEscondida = []
activacoesCamadaSaida = []

#treino...
treino = True
lerFicheiro = True
    
#ritmo de aprendizagem
ritmo_aprendizagem = 0.01
    
cicles = 10    
    
    
#estudo do erro
estudoErro = True
errosFinais = [0,0,0,0,0]




def funcaoSigmoide( valorEntrada):
    return 1.0 / (1.0 + math.exp((-1)*valorEntrada))

def funcaoDerivada( entrada):   
    return entrada*(1-entrada)



def retroPropagacao( arrayBits, valoresEsperados):
     
    print "OI == ",activacoesCamadaSaida 
    print "ARRAYbits == ", arrayBits, "valores esperados", valoresEsperados[0]
    desvios_saida = []
    for i in range(numeroNeuroniosSaida):
        print "I == ", i
        erro = valoresEsperados[i]-activacoesCamadaSaida[i]           
        derivada = funcaoDerivada(activacoesCamadaSaida[i])
        sigma = erro * derivada
        desvios_saida.append(ritmo_aprendizagem*sigma*activacoesCamadaEscondida[i])



    desvios_escondida = []
    for i in range(numeroNeuroniosEscondidos):
        derivada = activacoesCamadaEscondida[i]*(1-activacoesCamadaEscondida[i])
        somatorio = 0
        for j in range(numeroNeuroniosSaida):
            somatorio += ((-1)*desvios_saida[j])*pesosSaida[i][j]
        sigma = derivada * somatorio
        desvios_escondida.append(ritmo_aprendizagem*sigma*arrayBits[i])
        


    for i in range(numeroNeuroniosEscondidos):
        for j in range(numeroNeuroniosSaida):
            pesosSaida[i][j] += desvios_saida[j]
        
    for i in range(numeroEntradas):
        for j in range(numeroNeuroniosEscondidos):
            pesosEntrada[i][j] += desvios_escondida[j]


    if estudoErro:
        estudoDosErros(activacoesCamadaSaida, valoresEsperados)






def feedForward( arrayBits):


    #activacoesCamadaSaida = [] 
    for i in range(numeroNeuroniosEscondidos):
        somatorio = 0
        for j in range(numeroEntradas):
            somatorio += arrayBits[i] * pesosEntrada[j][i]
        activacoesCamadaEscondida.append(funcaoSigmoide(somatorio))


    for i in range(numeroNeuroniosSaida):
        somatorio = 0
        for j in range(numeroNeuroniosEscondidos):
            somatorio +=  pesosSaida[j][i] * activacoesCamadaEscondida[j]
        activacoesCamadaSaida.append(funcaoSigmoide(somatorio))
    #print

        print activacoesCamadaSaida


# Continue ... hades
def treino():
    error = 0
    # print "entradas globais ",numeroEntradas
    
    print input_teste
    for case in input_teste:
        print case[0] ,"->", case[1]
        input1= case[0]
        output = case[1]
        activacoesCamadaEscondida = []
        activacoesCamadaSaida = []
        feedForward(input1)
        retroPropagacao(input1, output)

# Starting hades .... 
    

def treinoRede():
   
    for iteration in range(cicles): 
        print "Iterac ", iteration
        treino()
        i+=1
        medias = []
        for elem in errosFinais:
            medias.append(elem/numeroCasos)
            print "- Media dos Erros Finais deste File: ",medias




    
def matrix_values_init():
        
    file1 = open('pesosEntrada.txt','r')
    file2 = open('pesosSaida.txt', 'r')
    
    # If Already exist consider the values ... 
    for i in range(numeroEntradas):
        if lerFicheiro:
            temp = file1.readline().split()
            for j in range(len(temp)):
                pesosEntrada[i][j] = float(temp[j]) 
                
        
    #else create news .... with random, it will be the weights of the first layer x second layer 
        else:
            for j in range(numeroNeuroniosEscondidos):
                pesosEntrada[i][j] = random.uniform(valorBaixo, valorAlto)
    # If Already exist consider the values ... 


    for i in range(numeroNeuroniosEscondidos):
        if lerFicheiro:
            temp = file2.readline().split()
            for j in range(numeroNeuroniosSaida):
                for x in range(len(temp)):
                    pesosSaida[i][j] = float(temp[x]) 

    #else create news .... with random, it will be the weights of the first layer x second layer 
        else:
            for j in range(numeroNeuroniosSaida):
                pesosSaida[i][j] = random.uniform(valorBaixo, valorAlto)







def matrix( I, J):
    matrix = []
    for i in range(I):
        pesos = []
        for j in range(J):
            pesos.append(0)
        matrix.append(pesos)
    return matrix


pesosEntrada = matrix(numeroEntradas, numeroNeuroniosEscondidos)
pesosSaida = matrix(numeroNeuroniosEscondidos, numeroNeuroniosSaida)
matrix_values_init()
if treino:
    treinoRede()
