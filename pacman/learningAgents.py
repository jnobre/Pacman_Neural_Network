from game import Agent
from random import choice
from util import loadFile, loadFilesFromList, loadFilesUntil, getActionRepresentation, getStateRepresentation
from game import Directions


import math
import random


class NeuralNetworkAgent(Agent):
  
    def __init__(self):
	self.movimentos = 0
	self.total_treino = 0
	self.media_erro_fim = 0
	self.treino_total = 0
	self.treino_erro_total = 0
	self.treinos = []
	self.menor_erro = 0
    
	self.resp_certa = 0
	self.resp_errada = 0
	self.resp_nao_conhecida = 0
	
	self.treino=[]
	self.verificar=[]
	self.teste=[]	

	self.ilegal_choice = 0.0
	self.ilegal_fchoice = 0.0
	self.ilegal_schoice = 0.0	

	self.entradas=[0.0]*20
	self.escondida=[0.0]*10
	self.saidas=[0.0]*5	
	
	#definir pesos entre entradas e camada escondida
	self.pesos1 =  [0.0]*len(self.escondida)
	
	#matriz usada na retropagacao para alterar os pesos entre camada escondida e saida
	self.tmp_muda1=[0.0]*len(self.saidas)
	for i in xrange(len(self.saidas)):
	    self.tmp_muda1[i]=[0.0]*len(self.escondida)	
	    
	#definir pesos entre camada escondida e saida
	self.pesos2 = [0.0]*len(self.saidas)
      
	#matriz usada na retropagacao para alterar os pesos entre camada entrada e escondida
	self.tmp_muda2=[0.0]*len(self.escondida)
	for i in xrange(len(self.escondida)):
	    self.tmp_muda2[i]=[0.0]*len(self.entradas)	 
	
	#carregar treinos
	testes=loadFilesUntil(50)
	for casos in testes:
	    for i in casos:
		self.total_treino = self.total_treino+1
		self.treinos.append(i)
	
	self.treinos = self.eliminar_rep()
	print "Numero de casos de teste unicos: ",len(self.treinos)
	
	#dividir treinos em 3 grupos
	self.num_treinos = int(math.ceil(len(self.treinos)*0.7))
	self.num_teste = int(math.ceil(len(self.treinos)*0.10))
	self.num_validacao = int(math.ceil(len(self.treinos)*0.20))		
	self.num_erro = int((self.num_treinos + self.num_teste + self.num_validacao) - int(self.total_treino))
	
	#adicionar cada um a sua lista
	for i in range(self.num_teste):
	    self.teste.append(self.treinos[i])
	i=self.num_teste
	for i in range(len(self.treinos)-(self.num_teste+self.num_validacao)):
	    self.treino.append(self.treinos[i])
	i=(self.num_treinos+self.num_teste)
	for i in range(len(self.treinos)- (self.num_treinos+self.num_teste)):
	    self.verificar.append(self.treinos[i])
	    
	#incializar pesos
	for i in xrange(len(self.escondida)):
	    self.pesos1[i]=[0.0]*len(self.entradas)
	    for j in xrange(len(self.entradas)):
		self.pesos1[i][j]=random.uniform(-0.5,0.5)
		
	i=0
	j=0
	for i in xrange(len(self.saidas)):
	    self.pesos2[i]=[0.0]*len(self.escondida)
	    for j in xrange(len(self.escondida)):
		self.pesos2[i][j]=random.uniform(-0.5,0.5)	
		
	#<---------------treinar rede neuronal------------------------->
	iteracao = 500
	maximo_i = 100
	incrementa = 0
	self.menor_erro = 1
	while (iteracao>0) and (self.menor_erro>0.0945):
	    

	    #<------treina-------->
	    erro = 0.0
	    for treinos in self.treino:
		input1=treinos[0]
		output=treinos[1]			
		self.propagacao(input1)
		erro = erro + self.retPropagacao(output, 0.1, 0.1)
	    #print "Erro final do treino: %-14f" % (erro / len(self.treino))
	    
	    #<------testa-------->
	    erro_testa = self.verificacao(self.teste)
	    #print "Erro teste iteracao: %-14f" %  (erro_testa)
	    
	    #<----dados estatisticos------>
	    self.treino_total = self.treino_total+float(500*len(self.treino))
	    self.treino_erro_total = self.treino_erro_total + erro_testa
	    
	    #se for maior que o min erro encontramos o menor erro
	    if(self.menor_erro < erro_testa) and (incrementa > 100):
		break;
	    
	    #verifica se erro de treino e menor que o minimo guardado
	    if(self.menor_erro > erro_testa):
		incrementa = 0
		self.menor_erro = erro_testa
	    else:
		incrementa = incrementa + 1
		
	    iteracao=iteracao-1
	    
	self.media_erro_fim = self.treino_erro_total  / len(self.treino)
	
	print "Erro na verificacao: %-14f" % (self.verificacao(self.verificar))
    
    def eliminar_rep(self):
	"""elimina casos de treino repetidos"""
	
	# cria um lista vazia
	aux = []
	aux.append(self.treinos[0])
	i=1
	# para cada valor da lista treinos se nao existir acrescenta no auxiliar
	for word in self.treinos:
	    if word not in aux:
		aux.append(word)
		i=i+1

	return aux
	
    def propagacao(self, input1):
	"""propagar rede neuronal x -> y -> z"""
	
	#inicializa array de entradas
	for i in xrange(len(self.entradas)):
	    self.entradas[i]=input1[i]	
	    
	#calcula valores dos neuronios da camada escondida atraves dos pesos
	for i in xrange(len(self.escondida)):
	    self.escondida[i] = 0.0
	    for j in xrange(len(self.entradas)):
		self.escondida[i]=self.escondida[i] + self.entradas[j] * self.pesos1[i][j]
	    self.escondida[i]=self.sigmoid(self.escondida[i])
	
	#calcula valores de neuronios da camada de saida atraves das saidas
	for i in xrange(len(self.saidas)):
	    self.saidas[i] = 0.0
	    for j in xrange(len(self.escondida)):
		self.saidas[i]=self.saidas[i] + self.escondida[j] * self.pesos2[i][j]
	    self.saidas[i]=self.sigmoid(self.saidas[i])	
	
	return self.saidas
    
    def retPropagacao(self,output,ritmo,momentum):
	"""desenvolve a retropropagacao"""
	
	if(len(output) != 5):
	    print "Saidas erradas!"
	    return 
	
	#calculo vector com erros na saida
	delta_3 = [0.0]*len(self.saidas)
	
	for i in xrange(len(self.saidas)):
	    erro = output[i] - self.saidas[i]
	    delta_3[i] =  self.derivada_sigmoid(self.saidas[i]) * erro
		    
	
	#calculo vector com erros na camada escondida 
	delta_2 = [0.0]*len(self.escondida)
	
	for i in xrange(len(self.escondida)):
	    erro = 0.0
	    for j in xrange(len(self.saidas)):
		erro = erro + delta_3[j]*self.pesos2[j][i]
	    delta_2[i] = self.derivada_sigmoid(self.escondida[i]) * erro
	    
	#actualiza pesos da camada 3 para a camada 2
	for i in xrange(len(self.escondida)):
	    for j in xrange(len(self.saidas)):
		tmp = delta_3[j]*self.escondida[i] #delta_minusculo3 *  valor do neuronio
		self.pesos2[j][i] = self.pesos2[j][i] + ritmo*tmp+momentum*self.tmp_muda1[j][i]
		self.tmp_muda1[j][i] = tmp	
	
	#actualiza pesos da camada 2 para a camada 1
	for i in xrange(len(self.entradas)):
	    for j in xrange(len(self.escondida)):
		tmp = delta_2[j]*self.entradas[i] #delta_minusculo2 *  valor do neuronio
		self.pesos1[j][i] = self.pesos1[j][i] + ritmo*tmp+momentum*self.tmp_muda2[j][i]
		self.tmp_muda2[j][i] = tmp
		
	#calcula soma de todos os erros
	erro = 0.0
	for i in xrange(len(output)):
	    erro = erro + 0.5*(output[i] - self.saidas[i]) ** 2
	return erro	
	
    def verificacao(self, testes):
	    """Verificacao do treino com casos de treino novos a rede"""
	    erro = 0.0
	    
	    for teste in testes:
		    input1 = teste[0]
		    output = teste[1]
		    self.propagacao(input1)
		    erro = erro + self.calc_erro(output)
	    
	    return erro/len(testes)    
    
    def calc_erro(self, saida_esp):
	"""Calcula o erro quadratico da rede"""	
	output_deltas = [0.0] * len(self.saidas)
		
	for i in range(len(self.saidas)):
	    erro = saida_esp[i] - self.saidas[i]
	    output_deltas[i] = self.derivada_sigmoid(self.saidas[i]) * erro
	    
	erro = 0.0
	for j in range(len(saida_esp)):
	    erro = erro + 0.5*(saida_esp[j]-self.saidas[j])**2
		
	return erro   

    
    def sigmoid(self, x):
        try:
            return 1.0/(1.0+math.exp(-x))
        except OverflowError:
			print "Value of x %-14f" % x 
			pass
		    
    def derivada_sigmoid(self, x):
	return self.sigmoid(x)*(1.0-self.sigmoid(x))
    
    def __del__(self):
	print "---- Estatisticas de treino ------------------------------------------------------------------"
	print "- Numero de casos de treino: ", self.total_treino
	print "- Media de erro final: %-14f" % self.media_erro_fim
	print "- Media de erro por output: %-14f" % (self.media_erro_fim/5)#media de erro / num de neuronio de saida
	print "- Real numero de Treino: ", int(self.treino_total)
	print "- Total erro sumado (treino): %-14f" % self.treino_erro_total
	print "- Media do total de erro (treino): %-14f" % (self.treino_erro_total/self.treino_total)
	print "---- Estatisticas do Jogo --------------------------------------------------------------------"
	print "- Numero de movimentos: ", int(self.movimentos)
	print "- Escolhas ilegais: ", int(self.ilegal_choice)
	print "- Numero de ilegal primeira escolhas: ", int(self.ilegal_fchoice)
	print "- Numero de ilegais alternativas: ", int(self.ilegal_schoice)
	print "- Media de movimentos ilegais: ", (self.ilegal_fchoice/self.movimentos)*100.0 , "%" 
	print "----------------------------------------------------------------------------------------"
	print "Cases: ", len(self.treinos), "%Train: ", self.num_treinos, " %Test: ", self.num_teste, " %Validation: ", self.num_validacao
	print "- Max (N-iteracoes): ", 500
	print "- Min Error (Train): ", self.menor_erro
	
	print "__________________________Relatorio____________________________________"
	print ""
	print "ESTATISTICAS DA REDE: "
	print "Somatorio de erro final: ", self.treino_erro_total
	print "Media do erro final: %-14f" % self.media_erro_fim
	print "Iteracoes: ", (1000 - 100)
	print "Treino (erro minimo): ", self.menor_erro
	print "Somatorio de erro final: %-14f" % self.treino_erro_total
	print "Media do erro final por saida: %-14f" % (self.treino_erro_total/self.treino_total)
	print ""	
	print "DADOS DO JOGADOR: "
	print "Numero de movimentos: ", int(self.movimentos)
	print "Movimentos ilegais: ", int(self.ilegal_choice)
	print "Percentagem de accoes ilegais: ", (self.ilegal_fchoice/self.movimentos)*100.0 , "%"	
	print "Padroes acertado ", self.resp_certa, " Percentagem -> ",100.0*(self.resp_certa/self.movimentos), "%"
	print "Padroes nao acertado ", self.resp_errada, " Percentagem -> ",100.0*(self.resp_errada/self.movimentos), "%"
	print "Padroes nao conhecido ", self.resp_nao_conhecida, " Percentagem -> ",100.0*(self.resp_nao_conhecida/self.movimentos), "%"
		
	
    def procura_output(self, caso, output):
	"""Procura output nos casos de treino"""
	for treinos in self.treinos:
	    if caso == treinos[0]:
		if output == treinos[1]:
		    return 1
		else:
		    return -1
		
	return 0


    def getAction(self, state):
	"""decidir decisao a tomar em cada instante do jogo"""
	
	#inicializa vector com 5 movimentos possiveis
	direcoes = [Directions.NORTH,Directions.SOUTH,Directions.EAST,Directions.WEST,Directions.STOP]
	
	self.movimentos=self.movimentos+1.0
	case=getStateRepresentation(state)
	output=self.propagacao(case)
		
	aux = output
	aux_dir = direcoes
	
	# troca directa
	# ordenar mudando o output e o array de direcoes    
	for i in xrange(len(aux)):
	    for j in xrange(i,len(aux)):
		if(aux[i]<aux[j]):
		    tmp = aux[i]
		    aux[i] = aux[j]
		    aux[j] = tmp
		    tmp = aux_dir[i]
		    aux_dir[i] = aux_dir[j]
		    aux_dir[j] = tmp
	
		    
	#percorre vector ordenado ate encontrar um movimento legal, executando esse mesmo movimento de seguida 
	for i in xrange(len(aux)):
	    if(i==0 and not aux_dir[i] in state.getLegalActions()):
		self.ilegal_fchoice=self.ilegal_fchoice+1.0
		self.ilegal_choice=self.ilegal_choice+1.0
	    elif not aux_dir[i] in state.getLegalActions():
		self.ilegal_schoice=self.ilegal_schoice+1.0
		self.ilegal_choice=self.ilegal_choice+1.0
	    elif aux_dir[i] in state.getLegalActions():
		move=aux_dir[i]
		break

	verifica = 0
	#converte direcao para respetivo array codificado
	output=getActionRepresentation(move)
	
	#verificar se acerta no padrao (acerta,erra,desconhece)
	verifica = self.procura_output(case,output)
	
	#contabiliza estatisticas em relacao aos padros
	if verifica == 1:
	    self.resp_certa += 1 
	elif verifica == -1:
	    self.resp_errada += 1
	elif verifica == 0:
	    self.resp_nao_conhecida += 1

	
	return move;	
        
    
    
    