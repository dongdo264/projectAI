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
        # Collect legal moves and successor states
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

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        """
        Chung ta quan tam den 3 khia canh:
        - khoang cach den ghost gan nhat, de tranh no ra
        - khoang cach den thuc an, pacman se an thuc an gan no nhat
        - so luong thuc an, he so phat giup no an het thuc an
        """
        """
        ghostCoef:
        - de pacman cang tranh xa ghost cang tot
        - trong khoang tu 1 den 20, tu 10 den 20 se dat diem cao nhat
        - neu he so qua cao, pacman se khong an duoc thuc an gan ghost
        """
        
        ghostDistance = 0
        capsuleScore = 0
        if len(currentGameState.getCapsules()) != 0:
            closestCapsule = min([manhattanDistance(capsule, newPos) for capsule in currentGameState.getCapsules()])
            if closestCapsule == 0:
                capsuleScore = 1000
            else:
                capsuleScore += 100/closestCapsule

        closestghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
        foodList = newFood.asList()
        if len(foodList) != 0:
            closestfood = min([manhattanDistance(newPos, food) for food in foodList])
        else:
            closestfood = 0

        if(sum(newScaredTimes) != 0):
            if closestghost <= 1:
                ghostDistance += 500
            else:
                ghostDistance = 500/closestghost
            score = (-1.4 * closestfood) + ghostDistance - (2*len(foodList)) + capsuleScore
        else:
            if closestghost <= 1:
                ghostDistance -= 1000
            else: 
                ghostDistance = -15/closestghost
            score = (-1.4 * closestfood) + ghostDistance - (100*len(foodList)) + capsuleScore
        return score
    
        return successorGameState.getScore()

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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # ***               max
        # ***           /-/  |   \--\
        # ***          /     |       \
        # ***         /      |        \  
        # ***      min1     min2      min3   
        # ***       /|\     /|\       /|\  
        # ***      / | \   / | \     / | \
        # ***     A  B  C D  E  F   G  H  I
        # ***     3 12  8 5  4  6   14 4  11 

        def minimaxSearch(state, agentIndex, depth):
            # Neu la min layer va la ghost cuoi dung
            if agentIndex == state.getNumAgents():
                # neu la max depth
                if depth == self.depth:
                    return self.evaluationFunction(state)
                else: 
                    # tao max layer voi depth = depth + 1
                    return minimaxSearch(state, 0, depth + 1)
            else:
                moves = state.getLegalActions(agentIndex)
                if len(moves) == 0:
                    return self.evaluationFunction(state)
                next = [minimaxSearch(state=state.generateSuccessor(agentIndex, move), agentIndex=(agentIndex + 1), depth=depth) for move in moves]
                if agentIndex == 0:
                    return max(next)
                else:
                    return min(next)
        return max(gameState.getLegalActions(0), key=lambda x: minimaxSearch(state=gameState.generateSuccessor(0,x), agentIndex=1, depth=1))

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

        def alphabeta(state):
            currentNode, bestAction, a, b = None, None, None, None
            for action in state.getLegalActions(0):
                currentNode = max(currentNode, nodeMin(state.generateSuccessor(0, action), 1, 1, a, b))
                if a is None:
                    a = currentNode
                    bestAction = action
                else:
                    a, bestAction = max(currentNode, a), action if currentNode > a else bestAction
                return bestAction
            
        def nodeMin(state, agentIndex, depth, a, b):
            if agentIndex == state.getNumAgents():
                return nodeMax(state, 0, depth + 1, a, b)
            temp_b = None
            for action in state.getLegalActions(agentIndex):
                currentNode = nodeMin(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth, a, b)
                if temp_b is None: temp_b = currentNode
                else: temp_b = min(currentNode, temp_b)

                if a is not None and temp_b < a:
                    return temp_b
                
                if b is None: b = temp_b
                else: b = min(temp_b, b)
            
            if temp_b is not None:
                return temp_b
            else:
                return self.evaluationFunction(state)
        
        def nodeMax(state, agentIndex, depth, a, b):
            if depth > self.depth:
                return self.evaluationFunction(state)
            temp_a = -9999999
            for action in state.getLegalActions(agentIndex):
                currentNode = nodeMin(state.generateSuccessor(agentIndex, action), agentIndex + 1, depth, a, b)
                temp_a = max(temp_a, currentNode)
                # tren node Max la node Min
                # Node min se update gia tri b
                # Neu a < b thi return luon a cat nhanh con lai
                if b is not None and temp_a > b:
                    return temp_a
                # nguoc lai, cap nhat gia tri max cua a
                a = max(a, temp_a)
            print(temp_a)
            if temp_a != -9999999:
                return temp_a
            else:
                return self.evaluationFunction(state)
        return alphabeta(gameState)

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

        def expectimaxSearch(state, agentIndex, depth):
            # Neu la min layer va la ghost cuoi dung
            if agentIndex == state.getNumAgents():
                # neu la max depth
                if depth == self.depth:
                    return self.evaluationFunction(state)
                # tao max layer voi depth = depth + 1
                else:
                    return expectimaxSearch(state, 0, depth + 1)
            else:
                moves = state.getLegalActions(agentIndex)
                if len(moves) == 0:
                    return self.evaluationFunction(state)
                next = [expectimaxSearch(state.generateSuccessor(agentIndex, m), agentIndex + 1, depth) for m in moves]

                if agentIndex == 0:
                    return max(next)
                else:
                    # khong dung min nua ma dung avg
                    return sum(next) / len(next)
        result = max(gameState.getLegalActions(0), key=lambda x: expectimaxSearch(gameState.generateSuccessor(0, x), 1, 1))

        return result
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    oldFood = currentGameState.getFood()

    """
    Chung ta quan tam den 3 khia canh:
    - khoang cach den ghost gan nhat, de tranh no ra
    - khoang cach den thuc an, pacman se an thuc an gan no nhat
    - so luong thuc an, he so phat giup no an het thuc an
    """
    """
    ghostCoef:
    - de pacman cang tranh xa ghost cang tot
    - trong khoang tu 1 den 20, tu 10 den 20 se dat diem cao nhat
    - neu he so qua cao, pacman se khong an duoc thuc an gan ghost
    """
    ghostDistance = 0
    capsuleScore = 0
    if len(currentGameState.getCapsules()) != 0:
        closestCapsule = min([manhattanDistance(capsule, newPos) for capsule in currentGameState.getCapsules()])
        if closestCapsule == 0:
            capsuleScore = 1000
        else:
            capsuleScore += 200/closestCapsule

    closestghost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])

    foodList = newFood.asList()
    if len(foodList) != 0:
        closestfood = min([manhattanDistance(newPos, food) for food in foodList])
    else:
        closestfood = 0

    if(sum(newScaredTimes) != 0):
        capsuleScore = -300
        if closestghost <= 1:
            ghostDistance += 350
        else:
            ghostDistance = 250/closestghost
        score = (-1.3 * closestfood) + ghostDistance - (3*len(foodList)) + capsuleScore
    else:
        if closestghost <= 1:
            ghostDistance -= 1000
        else: 
            ghostDistance = -15/closestghost
        score = (-1.3 * closestfood) + ghostDistance - (95*len(foodList)) + capsuleScore
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
