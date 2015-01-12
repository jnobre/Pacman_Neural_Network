"""
iiaAgents.py

Created by Rui Lopes on 2012-02-18.
Copyright (c) 2012 University of Coimbra. All rights reserved.
"""

from pacman import Directions, SCARED_TIME
from game import Agent

import random
import game
import util
from util import getActionRepresentation, getStateRepresentation
from array import *
"Variaveis de memoria usadas pelos agentes"
class evita_ciclos:
  DiREITA = 0
  ESQUERDA = 0
  OPOSTO = 0
  
  
  
class iiaPacmanAgent(Agent):	

  def __init__(self, index = 0):
    """iniciazilar agente aprendiz"""   
    self.index = index
    self.keys = []
    self.move = None
    self.treino = self.getTreino()
    print "Training name:", self.treino
    file = open(self.treino, 'w')
    file.close()    
    
  def getTreino(self):
    """devolver numero de treino"""
    import os.path
    name = "training_"
    count = 1
    while os.path.isfile(name + str(count) + ".iia"):
	    count += 1
    return name + str(count) + ".iia"   
  
  def saveTraining(self, currentStuff):
      import cPickle
      try:
	file = open(self.treino, 'r')
	oldStuff = cPickle.load(file)
	file.close()
      except EOFError:
	oldStuff = []
      file = open(self.treino, 'w')
      cPickle.dump(oldStuff + [currentStuff], file) 
      file.close()
    
  def threatTraining(self, move, state):
      
    from graphicsUtils import wait_for_keys
    
    legal = state.getLegalActions(self.index)
    stateRepresentation = getStateRepresentation(state)
	      
    print "State Representation:", stateRepresentation
 
    
    if move == None:
      print "Illegal move. Try again"
      
    actionRepresentation = getActionRepresentation(move)
    print "Action Representation:", actionRepresentation
    
    self.saveTraining([stateRepresentation, actionRepresentation])
      
  def getAction(self, state):
    fantasma = False
    posicao = state.getPacmanState().configuration.direction 
    px = state.getPacmanPosition()[0]
    py = state.getPacmanPosition()[1]    
    #sensor fantasma
    fantasma=self.sensorfantasma(state,posicao,px,py)
    #print "Tem Fantasma ? " , fantasma
    posicao = state.getPacmanState().configuration.direction
    """ esquerda = Directions.RIGHT[posicao]
    #print "ESQUERDA == ",left
    print "Direcao DIREITA == ", esquerda, " e a posicao corrente == ",posicao"""
    
    #<----- inicializacao dos valores da comida em cada direcao---->
    #variavel boolean confirma se existe comida 1a casa a frente na direcao
    quant_comidaFre = 0
    quant_comidaEsq = 0
    quant_comidaDir = 0
    #variavel que contem o valor de todas as comidas numa determinada direcao
    comidaDir = 0
    comidaEsq = 0
    comidaFre = 0
    #<----------------->
  
    #print "Comida == ",state.hasFood(px,py)
   
    quant_comidaFre,comidaFre=self.sensorcomidaFrente(state,posicao,px,py)
    quant_comidaEsq,comidaEsq=self.sensorcomidaEsquerda(state,posicao,px,py)
    quant_comidaDir,comidaDir=self.sensorcomidaDir(state,posicao,px,py)
    """ print "Quantidade comida direita == ", quant_comidaDir
    print "Comida na direita == "
    print comidaDir
    print "Quantidade comida Frente == ", quant_comidaFre
    print "Comida na Frente == "
    print comidaFre
    print "Quantidade comida Esquerda == ", quant_comidaEsq
    print "Comida na Esquerda == "
    print comidaEsq   """
    #if posicao == Directions.STOP: posicao = Directions.NORTH
    #<-------------------------AQUI---------------------------------------->
    if posicao == Directions.STOP: 
	  posicao = Directions.NORTH
    if fantasma == True:
      evita_ciclos.DIREITA = 0
      evita_ciclos.ESQUERDA = 0
      evita_ciclos.OPOSTO = 0
      if(Directions.RIGHT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.RIGHT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.RIGHT[posicao]
      elif(Directions.LEFT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.LEFT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.LEFT[posicao]
      else:
	evita_ciclos.OPOSTO = 1
	direcao = Directions.LEFT[Directions.LEFT[posicao]]
	self.threatTraining(direcao, state)	
	return Directions.LEFT[Directions.LEFT[posicao]]
          
    elif quant_comidaFre == True:
      evita_ciclos.DIREIRA = 0
      evita_ciclos.ESQUERDA = 0
      evita_ciclos.OPOSTO = 0    
      direcao = posicao
      self.threatTraining(direcao, state)      
      return posicao
   
    elif quant_comidaDir == True:
      evita_ciclos.DIREIRA=0
      evita_ciclos.ESQUERDA=0
      evita_ciclos.OPOSTO=0
      direcao = Directions.RIGHT[posicao]
      self.threatTraining(direcao, state)       
      return Directions.RIGHT[posicao]
   
    elif quant_comidaEsq == True:
      evita_ciclos.DIREITA = 0
      evita_ciclos.ESQUERDA = 0
      evita_ciclos.OPOSTO = 0
      direcao = Directions.LEFT[posicao]
      self.threatTraining(direcao, state)      
      return Directions.LEFT[posicao]
   
    elif (comidaDir>0) and (comidaDir >= comidaEsq) and (comidaDir >= comidaFre):
      evita_ciclos.DIREITA = 0
      evita_ciclos.ESQUERDA = 0
      evita_ciclos.OPOSTO = 0
      if(Directions.RIGHT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.RIGHT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.RIGHT[posicao]
      elif(Directions.LEFT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.RIGHT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.RIGHT[posicao]
      else:
	direcao = random.choice( state.getLegalActions(agent.index))
	self.threatTraining(direcao, state)	
	return random.choice( state.getLegalActions(agent.index))

    elif (comidaEsq>0) and (comidaEsq >= comidaDir) and (comidaEsq >= comidaFre):
      evita_ciclos.DIREITA = 0
      evita_ciclos.ESQUERDA = 0
      evita_ciclos.OPOSTO = 0      
      if(Directions.LEFT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.LEFT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.LEFT[posicao]
      elif(Directions.RIGHT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.RIGHT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.RIGHT[posicao]
      else: 
	direcao = random.choice( state.getLegalActions(agent.index)) 
	self.threatTraining(direcao, state)	
	return random.choice( state.getLegalActions(agent.index))      
    
    elif (comidaFre>0) and (comidaFre >= comidaDir) and (comidaFre >= comidaEsq):
      evita_ciclos.DIREITA = 0
      evita_ciclos.ESQUERDA = 0
      evita_ciclos.OPOSTO = 0        
      direcao = posicao
      self.threatTraining(direcao, state)
      return posicao

    elif(evita_ciclos.OPOSTO == 1):
      evita_ciclos.OPOSTO = 0
      
      if(Directions.LEFT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.LEFT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.LEFT[posicao]
      elif(Directions.RIGHT[posicao] in state.getLegalPacmanActions()):
	direcao = Directions.RIGHT[posicao]
	self.threatTraining(direcao, state)	
	return Directions.RIGHT[posicao]
      elif posicao in state.getLegalPacmanActions(): 
	direcao = posicao
	self.threatTraining(direcao, state)	
	return posicao 
      else: 
	#<---------------------------AQUI---------------------------->
	direcao = Directions.LEFT[Directions.LEFT[posicao]]
	self.threatTraining(direcao, state)	
	return Directions.LEFT[Directions.LEFT[posicao]]
    
    elif posicao in state.getLegalPacmanActions():

      evita_ciclos.OPOSTO = 0
      direcao = posicao
      self.threatTraining(direcao, state)      
      return posicao
    
    elif(Directions.RIGHT[posicao] in state.getLegalPacmanActions()) and evita_ciclos.DIREITA<4:
      evita_ciclos.DIREITA = evita_ciclos.DIREITA+1
      evita_ciclos.ESQUERDA = 0
      direcao = Directions.RIGHT[posicao]
      self.threatTraining(direcao, state)     
      return Directions.RIGHT[posicao]
    
    elif(Directions.LEFT[posicao] in state.getLegalPacmanActions()) and evita_ciclos.ESQUERDA<4:
      evita_ciclos.ESQUERDA = evita_ciclos.ESQUERDA+1
      evita_ciclos.DIREITA = 0      
      direcao = Directions.LEFT[posicao]
      self.threatTraining(direcao, state)      
      return Directions.LEFT[posicao]
    
    elif(Directions.LEFT[Directions.LEFT[posicao]] in state.getLegalPacmanActions()):
      evita_ciclos.ESQUERDA = 0
      evita_ciclos.DIREITA = 0       
      evita_ciclos.OPOSTO = 1
      direcao = Directions.LEFT[Directions.LEFT[posicao]]
      self.threatTraining(direcao, state)
      return Directions.LEFT[Directions.LEFT[posicao]]
    
    else:
      direcao = Directions.STOP
      self.threatTraining(direcao, state)       
      return Directions.STOP
      
    #return random.choice( state.getLegalPacmanActions() )


    
  def sensorcomidaEsquerda(self,state,posicao,px,py):
    """verifica se existe comida a esquerda"""
    comidaEsquerda=0
    quant_comidaEsquerda=0
   # print "Posicao actual == ", posicao
    if posicao == Directions.WEST : 
      y=py-1
      while (state.hasWall(px,y)!=1):
	if(state.hasFood(px,y)): 
	  comidaEsquerda=comidaEsquerda+1
	y=y-1
      quant_comidaEsquerda = state.hasFood(px,py-1)
    elif posicao == Directions.NORTH : 
      x=px-1
      while (state.hasWall(x,py)!=1):
	if(state.hasFood(x,py)): 
	  comidaEsquerda=comidaEsquerda+1
	x=x-1
      quant_comidaEsquerda = state.hasFood(px-1,py)
    elif posicao == Directions.EAST : 
      y=py+1
      while (state.hasWall(px,y)!=1):
	if(state.hasFood(px,y)): 
	  comidaEsquerda=comidaEsquerda+1
	y=y+1
      quant_comidaEsquerda = state.hasFood(px,py+1)
    else : 
      x=px+1
      while (state.hasWall(x,py)!=1):
	if(state.hasFood(x,py)): 
	  comidaEsquerda=comidaEsquerda+1
	x=x+1
      quant_comidaEsquerda = state.hasFood(px+1,py)    
    return quant_comidaEsquerda,comidaEsquerda
    
    
  def sensorcomidaFrente(self,state,posicao,px,py):
    """verifica se existe comida a sua frente"""
    comidaFrente = 0
    quant_comidaFrente = 0
    #print "Posicao actual == ", posicao
    if posicao == Directions.WEST : 
		    x=px-1
		    while(state.hasWall(x,py)!=1):
			    if(state.hasFood(x,py)): 
				    comidaFrente = comidaFrente+1
			    x=x-1
		    quant_comidaFrente = state.hasFood(px-1,py)
    elif posicao == Directions.NORTH : 
		    y=py+1
		    while(state.hasWall(px,y)!=1):
			    if(state.hasFood(px,y)): 
				    comidaFrente=comidaFrente+1
			    y=y+1
		    quant_comidaFrente = state.hasFood(px,py+1)
    elif posicao == Directions.EAST : 
		    x=px+1
		    while(state.hasWall(x,py)!=1):
			    if(state.hasFood(x,py)): 
				    comidaFrente=comidaFrente+1
			    x=x+1
		    quant_comidaFrente = state.hasFood(px+1,py)
    else : 
		    y=py-1
		    while(state.hasWall(px,y)!=1):
			    if(state.hasFood(px,y)): 
				    comidaFrente=comidaFrente+1
			    y=y-1
		    quant_comidaFrente = state.hasFood(px,py-1)
      
    return quant_comidaFrente,comidaFrente
     
	
  def sensorcomidaDir(self,state,posicao,px,py):
    """verfica se existe comida a frente"""
    comidaDir=0
    quant_comidaDir=0
    if posicao == Directions.WEST : 
      y=py+1
      while (state.hasWall(px,y)!=1):
	if(state.hasFood(px,y)): 
	  comidaDir=comidaDir+1
	y=y+1
      quant_comidaDir = state.hasFood(px,py+1)
    elif posicao == Directions.NORTH : 
      x=px+1
      while (state.hasWall(x,py)!=1):
	if(state.hasFood(x,py)): 
	  comidaDir=comidaDir+1
	x=x+1
      quant_comidaDir = state.hasFood(px+1,py)
    elif posicao == Directions.EAST : 
      y=py-1
      while (state.hasWall(px,y)!=1):
	if(state.hasFood(px,y)): 
	  comidaDir=comidaDir+1
	y=y-1
      quant_comidaDir = state.hasFood(px,py-1)
    else : 
      x=px-1
      while (state.hasWall(x,py)!=1):
	if(state.hasFood(x,py)): 
	  comidaDir=comidaDir+1
	x=x-1
      quant_comidaDir = state.hasFood(px-1,py)   
      
    return quant_comidaDir,comidaDir
    
  def sensorfantasma(self,state,posicao,px,py):
    """verifica se existe fantasma"""
    legal = state.getLegalPacmanActions()
    #posicao = state.getPacmanState().configuration.direction 
    encontrou = False;
    nrfantasma = state.getNumAgents()

    #print " X == ",px," Y == ",py
    #verificar se ha fantasma a frente
    for i in range(1,nrfantasma):
      gx = state.getGhostPosition(i)[0]
      gy = state.getGhostPosition(i)[1]
   # print "HA PARADE == ",state.hasWall(px-1,py)
      if(posicao == Directions.WEST and state.hasWall(px-1,py) != 1 and state.hasWall(px-2,py) != 1 and ((px-2 <=gx and gx < px and py == gy) or (px-1 == gx and py == gy) or (px-1 == gx and py+1 == gy) or (px-1 == gx and py-1 == gy))):

	encontrou = True

      elif(posicao == Directions.WEST and ((px -2 <= gx and gx<px and py == gy) or (px-1 == gx and py == gy) or (px-1 == gx and py-1 == gy))):

	encontrou = True

      elif(posicao == Directions.NORTH and state.hasWall(px,py+1)!=1 and state.hasWall(px,py+2)!=1 and ((px == gx and py+2 >= gy and gy > py) or (px == gx and py+1 == gy) or (px-1 == gx and py+1 == gy))):

	encontrou = True
      
      elif(posicao == Directions.NORTH and ((px == gx and py+2 >= gy and gy > py) or (px == gx and py+1 == gy) or (px-1 == gx and py+1 == gy))):

	encontrou = True
        
      elif (posicao == Directions.EAST and state.hasWall(px+1,py)!=1  and state.hasWall(px+2,py)!=1 and ((px+2 >= gx and gx>px and py == gy ) or (px+1 == gx and py == gy ) or (px+1 == gx and py+1 == gy) or (px+1 == gx and py-1 == gy))) : 

	encontrou = True
      
      elif (posicao == Directions.EAST  and ((px+2 >= gx and gx>px and py == gy ) or (px+1 == gx and py == gy ) or (px+1 == gx and py+1 == gy) or (px+1 == gx and py-1 == gy))):
	
	encontrou = True
      
      elif (posicao == Directions.SOUTH and state.hasWall(px,py-1)!=1 and state.hasWall(px,py-2)!=1 and ((px == gx and py-2 <= gy and gy<py) or ( px == gx and py-1 == gy) or (px-1 == gx and py-1 == gy) or (px+1 == gx and py-1 == gy))):
	
	encontrou = True
      
      elif(posicao == Directions.SOUTH and ((px == gx and py-2 <= gy and gy<py) or ( px == gx and py-1 == gy) or (px-1 == gx and py-1 == gy) or (px+1 == gx and py-1 == gy))):
	
	encontrou = True
  
      if(encontrou == True) and (state.getGhostState(i).scaredTimer>0): 
	encontrou = False
    
    return encontrou
  
  
  
class iiaGhostAgent(Agent):	 
  """Uses a strategy pattern to allow usage of different ghost behaviors in the game. 
  The strategy must receive an agent and a GameState as the arguments.
  To set the strategy through command line use:
  >>>pacman.py -g iiaGhostAgent --ghostArgs fnStrategy='fun1[;fun*]'
  You may add new arguments as long as you provide a proper constructor. """
  def __init__(self, index, fnStrategy='defaultstrategy'):
    self.index=index
    strategies = fnStrategy.split(';')
    try:
      self.strategy = util.lookup(strategies[index%len(strategies)], globals())
    except:
      print "Function "+strategies[index%len(strategies)]+" not defined!"
      print "Loading defaultstrategy..."
      self.strategy = defaultstrategy
 
  def getAction(self, state):
    """The agent receives a GameState (defined in pacman.py).
     Simple random ghost agent."""
    return self.strategy( self, state )  
 


#sensor procura pacman no campo de visao
def findpath(x,y,direction,state):
    px,py = state.getPacmanPosition()
    walls = state.getWalls()
    if (direction==Directions.EAST):
        x=x+1
        while walls[x][y]== False:       
            if((x == px) and (y == py)):
                return -1
            else:
                x=x+1
                
    elif(direction==Directions.WEST):
        x=x-1
        while walls[x][y]== False:
            if((x == px) and (y == py)):
                return -1
            else:
                x=x-1
                
    elif(direction==Directions.NORTH):
        y=y+1
        while walls[x][y]== False:        
            if((x == px) and (y == py)):
                return -1
            else:
                y=y+1
                
    elif(direction==Directions.SOUTH):
        y=y-1
        while walls[x][y]== False:         
            if((x == px) and (y == py)):
                return -1
            else:
                y=y-1
    
    return 0
 

#sensor se encontrar fantasma tenta fugir
def sensorghost_escape(x,y,agent,state,direction):

       
    if(direction!=Directions.WEST):
        if (findpath(x,y,Directions.EAST,state)==-1):
            #percorre todas as possibilidades
            for i in state.getLegalActions(agent.index):
                if(i != Directions.EAST):
                    return i;
        
        
    if(direction!=Directions.EAST):
        if (findpath(x,y,Directions.WEST,state)==-1):
            for i in state.getLegalActions(agent.index):
                if(i != Directions.WEST):
                    return i;
        
    if(direction!=Directions.SOUTH):
        if (findpath(x,y,Directions.NORTH,state)==-1):
            for i in state.getLegalActions(agent.index):
                if(i != Directions.NORTH):
                    return i;  
    
    if(direction!=Directions.NORTH):
        if (findpath(x,y,Directions.SOUTH,state)==-1):
            for i in state.getLegalActions(agent.index):
                if(i != Directions.SOUTH):
                    return i;  


    return random.choice(state.getLegalActions(agent.index))          

#funcao que define comportamente do fantasma o direto
def crazystrategy(agent,state):
  
    # Fantasma "O Directo"
    teste=state.getGhostState(agent.index)
    direction=teste.getDirection()

    x,y=(teste.getPosition())
    x=int(x)
    y=int(y)
    
    #pacman pode comer
    if(teste.scaredTimer>0):
        #print state.getLegalActions(agent.index)
        #sensor para escapar do pacman 
        return sensorghost_escape(x,y,agent,state,direction)
    else:
      #a busca do pacman
        if(direction!=Directions.WEST):
            if (findpath(x,y,Directions.EAST,state)==-1) and (Directions.EAST in state.getLegalActions(agent.index)):
                return Directions.EAST
      
        if(direction!=Directions.EAST):
            if (findpath(x,y,Directions.WEST,state)==-1) and (Directions.WEST in state.getLegalActions(agent.index)):
                return Directions.WEST
      
        if(direction!=Directions.SOUTH):
            if (findpath(x,y,Directions.NORTH,state)==-1) and (Directions.NORTH in state.getLegalActions(agent.index)):
                return Directions.NORTH
      
        if(direction!=Directions.NORTH):
            if (findpath(x,y,Directions.SOUTH,state)==-1) and (Directions.SOUTH in state.getLegalActions(agent.index)):
                return Directions.SOUTH
      
    return random.choice(state.getLegalActions(agent.index))

  
def defaultstrategy(agent,state):
  	print state.getLegalActions(agent.index)
	return random.choice( state.getLegalActions(agent.index))
  

  
