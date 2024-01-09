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
        foodDistance=[]
        scaredTimes=[]
        for ghost in successorGameState.getGhostStates():
            ghostDistance=[manhattanDistance(ghost.getPosition(),newPos)]
            scaredTimes.append(ghost.scaredTimer)
            if ghost.scaredTimer!=0:
                return 1/(5*min(ghostDistance)) #When scared timer is not zero, pacman gets incentive to eat ghost.
        for food in newFood.asList():
            foodDistance.append(manhattanDistance(food,newPos))
        if len(foodDistance)==0: #if there is no food left, the agent has won. The board is clear
            return 10000000 #high number to reward clearing the board
        else:
             closestFood=min(foodDistance) #if pacman is far away from the closest food, then we will penalize pacman.
        if min(ghostDistance)<4: #penalize if the agent gets too close to the ghost
            return -10000000
        return successorGameState.getScore()+max(newScaredTimes) +1/closestFood #Reciprocal because if pacman is far away from the closest food, then we will penalize pacman.
        # return max(max(newScaredTimes),min(distances))
        # return successorGameState.getScore()+max(newScaredTimes)

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
        # Format of result = [score, action]
        return self.MiniMax(gameState, 0, 0)[1]

    def MiniMax(self, gameState, index, depth):
        # Check if game is won or lost or if leaf nodes are reached
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth* (gameState.getNumAgents()):
            return self.evaluationFunction(gameState), ""
        #If not terminal node or game is not over, call the function
        return self.max_minValue(gameState,index, depth)
    
    def max_minValue(self, gameState,index, depth):
        """
        Returns the utility value-action for max-agent and min-agent based on index
        """
        Moves = gameState.getLegalActions(index)
        max_value = float("-inf")
        min_value=float("inf") 
        optimal_action = ""
        num_agents=gameState.getNumAgents()

        if index==0:
            for action in Moves:
                current_value = self.MiniMax(gameState.generateSuccessor(0, action), (depth+1)%num_agents, depth+1)[0]
                if current_value > max_value:
                    max_value = current_value
                    optimal_action = action
            return max_value, optimal_action
        else:
            for action in Moves:
                current_value = self.MiniMax(gameState.generateSuccessor(index, action), (depth+1)%num_agents, depth+1)[0]
                if current_value < min_value:
                    min_value = current_value
                    optimal_action = action
            return min_value, optimal_action
    
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBeta(gameState, 0, 0,-float("inf"),float("inf"))[1]
    
    def alphaBeta(self, gameState, index, depth, alpha, beta):
        # Check if game is won or lost or if leaf nodes are reached
        if len(gameState.getLegalActions(index)) == 0 or depth == self.depth* (gameState.getNumAgents()):
            return self.evaluationFunction(gameState), ""

        #For non terminal States 
        
        return self.alpha_betaValue(gameState, index, depth, alpha, beta)


    def alpha_betaValue(self, gameState,index, depth, alpha, beta):
        """
        Returns the utility value-action for agent based on index
        """
        Moves = gameState.getLegalActions(index)
        max_value = -float("inf")
        min_value = float("inf")
        optimal_action = ""

        num_agents=gameState.getNumAgents()
        if index==0:
            for action in Moves:
                current_value = self.alphaBeta(gameState.generateSuccessor(0, action), (depth+1)%num_agents, depth+1, alpha, beta)[0]
                if current_value > max_value:
                    max_value = current_value
                    optimal_action = action
                
                alpha=max(alpha, max_value)
                if max_value > beta:
                    return max_value, optimal_action
            return max_value, optimal_action
        else:
            for action in Moves:
                current_value = self.alphaBeta(gameState.generateSuccessor(index, action), (depth+1)%num_agents, depth+1, alpha, beta)[0]
                if current_value < min_value:
                    min_value = current_value
                    optimal_action = action
                
                beta=min(beta, min_value)
                if min_value < alpha:
                    return min_value, optimal_action
            return min_value, optimal_action

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
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
