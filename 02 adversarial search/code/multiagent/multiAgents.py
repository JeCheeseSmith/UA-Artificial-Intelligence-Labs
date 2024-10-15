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
import math

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        #newGhostStates = successorGameState.getGhostStates()
        #newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        #Calc closest ghost
        ghostPositions = [state.getPosition() for state in successorGameState.getGhostStates()]
        closest_ghost_distance = min(manhattanDistance(newPos, ghost_pos ) for ghost_pos in ghostPositions)
        closest_ghost_distance = -math.inf if closest_ghost_distance == 0 else closest_ghost_distance

        #Calc closest foods
        foods = newFood.asList()
        closest_food_dist = min(manhattanDistance(newPos, food_pos) for food_pos in foods) if foods else 0

        score = successorGameState.getScore() + closest_ghost_distance - closest_food_dist
        return score

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        best_val, best_action = self.value(gameState, agentIdx=0, remainingDepth=self.depth)
        return best_action

    def max_value(self, state, agentIdx, remainingDepth):
        assert agentIdx == 0

        best_val = - math.inf
        best_action = None
        legal_actions = state.getLegalActions(agentIdx)
        for act in legal_actions:
            successor = state.generateSuccessor(agentIdx, act)
            val, _ = self.value(successor, (agentIdx + 1) % state.getNumAgents(), remainingDepth)
            if best_val < val:  # max
                best_val = val
                best_action = act

        return best_val, best_action

    def min_value(self, state, agentIdx, remainingDepth):
        assert agentIdx > 0

        # decr reaming depth for final ghost
        if agentIdx == state.getNumAgents() - 1:
            remainingDepth -= 1

        best_val = + math.inf
        best_action = None
        legal_actions = state.getLegalActions(agentIdx)
        for act in legal_actions:
            successor = state.generateSuccessor(agentIdx, act)
            val, _ = self.value(successor, (agentIdx + 1) % state.getNumAgents(), remainingDepth)
            if best_val > val:  # min
                best_val = val
                best_action = act

        return best_val, best_action

    def value(self, state, agentIdx, remainingDepth):
        if state.isWin() or state.isLose() or remainingDepth == 0:  # Terminal
            return self.evaluationFunction(state), None
        elif agentIdx == 0:  # Max
            return self.max_value(state, agentIdx, remainingDepth)
        else:  # Min
            return self.min_value(state, agentIdx, remainingDepth)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        super().__init__(evalFn, depth)
        self.alfa = - math.inf
        self.beta = + math.inf

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        best_val, best_action = self.value(gameState, 0, self.depth, self.alfa, self.beta)
        return best_action

    def max_value(self, state, agentIdx, remainingDepth, alfa, beta):
        assert agentIdx == 0
        best_val = - math.inf
        best_action = None
        legal_actions = state.getLegalActions(agentIdx)

        for act in legal_actions:
            successor = state.generateSuccessor(agentIdx, act)
            val, _ = self.value(successor, (agentIdx + 1) % state.getNumAgents(), remainingDepth, alfa, beta)
            if best_val < val:  # max
                best_val = val
                best_action = act
            if best_val > beta:
                return best_val, best_action
            alfa = max(alfa, best_val)

        return best_val, best_action

    def min_value(self, state, agentIdx, remainingDepth, alfa, beta):
        assert agentIdx > 0

        # decr reaming depth for final ghost
        if agentIdx == state.getNumAgents() - 1:
            remainingDepth -= 1

        best_val = + math.inf
        best_action = None
        legal_actions = state.getLegalActions(agentIdx)
        for act in legal_actions:
            successor = state.generateSuccessor(agentIdx, act)
            val, _ = self.value(successor, (agentIdx + 1) % state.getNumAgents(), remainingDepth, alfa, beta)
            if best_val > val:  # min
                best_val = val
                best_action = act
            if best_val < alfa:
                return best_val, best_action
            beta = min(beta, best_val)

        return best_val, best_action

    def value(self, state, agentIdx, remainingDepth, alfa, beta):
        if state.isWin() or state.isLose() or remainingDepth == 0:  # Terminal
            return self.evaluationFunction(state), None
        elif agentIdx == 0:  # Max
            return self.max_value(state, agentIdx, remainingDepth, alfa, beta)
        else:  # Min
            return self.min_value(state, agentIdx, remainingDepth, alfa, beta)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        best_val, best_action = self.value(gameState, agentIdx=0, remainingDepth=self.depth)
        return best_action

    def max_value(self, state, agentIdx, remainingDepth):
        assert agentIdx == 0

        best_val = - math.inf
        best_action = None
        legal_actions = state.getLegalActions(agentIdx)
        for act in legal_actions:
            successor = state.generateSuccessor(agentIdx, act)
            val, _ = self.value(successor, (agentIdx + 1) % state.getNumAgents(), remainingDepth)
            if best_val < val:  # max
                best_val = val
                best_action = act

        return best_val, best_action

    def exp_value(self, state, agentIdx, remainingDepth):
        assert agentIdx > 0

        # decr reaming depth for final ghost
        if agentIdx == state.getNumAgents() - 1:
            remainingDepth -= 1

        best_val = 0
        best_action = None
        legal_actions = state.getLegalActions(agentIdx)
        for act in legal_actions:
            successor = state.generateSuccessor(agentIdx, act)
            val, _ = self.value(successor, (agentIdx + 1) % state.getNumAgents(), remainingDepth)
            best_val += val  # Assuming probability p == 1

        return best_val/len(legal_actions), best_action

    def value(self, state, agentIdx, remainingDepth):
        if state.isWin() or state.isLose() or remainingDepth == 0:  # Terminal
            return self.evaluationFunction(state), None
        elif agentIdx == 0:  # Max
            return self.max_value(state, agentIdx, remainingDepth)
        else:  # Min
            return self.exp_value(state, agentIdx, remainingDepth)

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
