# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        Foodlist=newFood.asList()
        DirectionGhost=childGameState.getGhostPositions()
        gd=0
        sum=0
        for food in Foodlist:
            
            sum=sum+manhattanDistance(food,newPos)

        for ghost in DirectionGhost:
            
            if(manhattanDistance(newPos,ghost)<=1):         #avoid ghosts at all costs
                return -10000000000000000
            else:
                gd=gd+manhattanDistance(newPos,ghost)       #save distance of all ghosts

        if(gd<len(DirectionGhost)*2):                      #don't let many ghosts get too close to you
            return -100000000000000000
        
                
            
        if len(Foodlist)<1:                                #if you ate the last pelet give huge score
            return 100000000000000000000
        add=0
        if currentGameState.getPacmanPosition()!=newPos:
            add=100                                          #give a nodge so that pacman doesn't stay still, also it kind of looks like it's mocking the ghosts


        score=100000*(1000-len(Foodlist))-sum+add          #emptying the pelets is much more important than the pelets being close
        return score

        



        return childGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maxv(gameState,depth):
            pind=0
            gotactions=gameState.getLegalActions(pind)
            if gameState.isWin():                                   #won
                return(self.evaluationFunction(gameState),None)
            elif  gameState.isLose():                               #lost
                return(self.evaluationFunction(gameState),None)
            elif depth==self.depth:                                 #reached bottom
                return(self.evaluationFunction(gameState),None)
            elif len(gotactions)<1 :                                #no more actions
                return(self.evaluationFunction(gameState),None)
            else:
                score=-10000000
                a=None                                                                               
                for action in gotactions:                                                                         
                    nextaction=gameState.getNextState(pind,action)      #pacman plays so index pind=0
                    v=minv(nextaction,1,depth)                          
                    if(v[0]>score):                                 #keep the biggest score
                        score=v[0]
                        a=action
                return(score,a)

        def minv(gameState,ghost,depth):
            gotactions=gameState.getLegalActions(ghost)
            if len(gotactions) == 0:
                return(self.evaluationFunction(gameState),None)         #no more actions
            score=10000000                                                                                  
            a=None
            for action in gotactions:
                amountgh=gameState.getNumAgents()
                if(ghost==amountgh-2):
                    v=minv(gameState.getNextState(ghost,action),ghost+1,depth)      #recursivelly go to next condition for every ghost
                elif(ghost==amountgh-1):
                    v=maxv(gameState.getNextState(ghost,action),depth + 1)  #keep the biggest score of pacman for this ghost action
                if(v[0]<score):                                        #keep smallest score
                    score=v[0]
                    a=action
            return(score,a)

        return maxv(gameState,0)[1]                 #return the action that returns biggest value at depth 0

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"


        def maxv(gameState,depth,a,b):
            pind=0
            gotactions=gameState.getLegalActions(pind)
            if gameState.isWin():                                   #won
                return(self.evaluationFunction(gameState),None)
            elif  gameState.isLose():                               #lost
                return(self.evaluationFunction(gameState),None)
            elif depth==self.depth:                                 #reached bottom
                return(self.evaluationFunction(gameState),None)
            elif len(gotactions)<1 :                                #no more actions
                return(self.evaluationFunction(gameState),None)
            else:
                score=-10000000
                ac=None                                                                               
                for action in gotactions:                                                                         
                    nextaction=gameState.getNextState(pind,action)      #pacman plays so index pind=0
                    v=minv(nextaction,1,depth,a,b)                          
                    if(v[0]>score):                                 #keep the biggest score
                        score=v[0]
                        ac=action
                    if(b<score):
                        return(score,action)
                    if(a<score):
                        a=score
            return(score,ac)

        def minv(gameState,ghost,depth,a,b):
            gotactions=gameState.getLegalActions(ghost)
            if len(gotactions) == 0:
                return(self.evaluationFunction(gameState),None)         #no more actions
            score=10000000                                                                                  
            ac=None
            for action in gotactions:
                amountgh=gameState.getNumAgents()
                if(ghost==amountgh-2):
                    v=minv(gameState.getNextState(ghost,action),ghost+1,depth,a,b)      #recursivelly go to next condition for every ghost
                elif(ghost==amountgh-1):
                    v=maxv(gameState.getNextState(ghost,action),depth + 1,a,b)  #keep the biggest score of pacman for this ghost action
                if(v[0]<score):                                        #keep smallest score
                    score=v[0]
                    ac=action
                if(a>score):
                    return(score,ac)
                if(b>score):
                        b=score
            return(score,ac)
        return maxv(gameState,0,-10000000,10000000)[1]                 #return the action that returns biggest value at depth 0

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def maxv(gameState,depth):
            pind=0
            gotactions=gameState.getLegalActions(pind)
            if gameState.isWin():                                   #won
                return(self.evaluationFunction(gameState),None)
            elif  gameState.isLose():                               #lost
                return(self.evaluationFunction(gameState),None)
            elif depth==self.depth:                                 #reached bottom
                return(self.evaluationFunction(gameState),None)
            elif len(gotactions)<1 :                                #no more actions
                return(self.evaluationFunction(gameState),None)
            else:
                score=-10000000
                a=None                                                                               
                for action in gotactions:                                                                         
                    nextaction=gameState.getNextState(pind,action)      #pacman plays so index pind=0
                    v=minv(nextaction,1,depth)                          
                    if(v[0]>score):                                 #keep the biggest score
                        score=v[0]
                        a=action
                return(score,a)

        def minv(gameState,ghost,depth):
            gotactions=gameState.getLegalActions(ghost)
            if len(gotactions) == 0:
                return(self.evaluationFunction(gameState),None)         #no more actions
            score=10000000                                                                                  
            a=None
            for action in gotactions:
                amountgh=gameState.getNumAgents()
                if(ghost==amountgh-2):
                    v=minv(gameState.getNextState(ghost,action),ghost+1,depth)      #recursivelly go to next condition for every ghost
                elif(ghost==amountgh-1):
                    v=maxv(gameState.getNextState(ghost,action),depth+1)  #keep the biggest score of pacman for this ghost action at the next depth
                score+=v[0]/len(gotactions)
                a=action
            return(score,a)

        return maxv(gameState,0)[1]                 #return the action that returns biggest value at depth 0

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <I take into consideration the amount of food, capsules and score to get my number, while also,
    avoiding the ghost if it is close to me and i haven't eaten a capsule, or chasing it if i have. My number is
    boosted up if i win and down if i lose. Usually when there are few pellets remaining i wait for the ghost to
    chase me, because I could't find a way to fight that and get a better score.>
    """
    "*** YOUR CODE HERE ***"

    #we multiply according to value, more zeroes, means it is more important

    score=0
    score+=100000 * currentGameState.getScore()                  #the bigger the score, the better
    score+=-10000000*(len(currentGameState.getCapsules()))          #capsules give score boost, better to eat them
    for food in currentGameState.getFood().asList():                                    #the less the food, the bigger the score
        score += -manhattanDistance(currentGameState.getPacmanPosition(), food)
    for ghost in currentGameState.getGhostPositions():
        if manhattanDistance(currentGameState.getPacmanPosition(),ghost)<2:             #if ghosts are bad, avoid them, else you can eat them if they are close, if not ignore them
            for scared in [ghostState.scaredTimer for ghostState in currentGameState.getGhostStates()]:
                if scared==0:
                    score+=-1000*(10-manhattanDistance(currentGameState.getPacmanPosition(),ghost))
                else:
                    score+=1000*(10-manhattanDistance(currentGameState.getPacmanPosition(),ghost))



    if currentGameState.isWin():                    #win gives huge score boost, loss the opposite
        score+=100000000
    elif currentGameState.isLose():
        score=-100000000
    return score

    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
