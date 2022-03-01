import random

from pacai.agents.base import BaseAgent
from pacai.agents.search.multiagent import MultiAgentSearchAgent


class ReflexAgent(BaseAgent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.
    You are welcome to change it in any way you see fit,
    so long as you don't touch the method headers.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        `ReflexAgent.getAction` chooses among the best options according to the evaluation function.

        Just like in the previous project, this method takes a
        `pacai.core.gamestate.AbstractGameState` and returns some value from
        `pacai.core.directions.Directions`.
        """
        # increase value of food
        # Collect legal moves.
        # remove stop from actions
        legalMoves = gameState.getLegalActions()
        if "Stop" in legalMoves:
            legalMoves.remove("Stop")
        # Choose one of the best actions.
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best.
        # remove stop from actions

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current `pacai.bin.pacman.PacmanGameState`
        and an action, and returns a number, where higher numbers are better.
        Make sure to understand the range of different values before you combine them
        in your evaluation function.
        """

        successorGameState = currentGameState.generatePacmanSuccessor(action)

        # Useful information you can extract.
        newPosition = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        # for food in oldfood , add certain score for food/ (distance to that food)
        # subract from score if ghost near by

        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.getScaredTimer() for ghostState in newGhostStates]

        # *** Your Code Here ***

        # for food in oldfood , add certain score for food/ (distance to that food)
        # subract from score if ghost near by
        # return own score , positive for closeness to food, negative for closeness to ghost

        from pacai.core.distance import manhattan

        score = successorGameState.getScore()
        oldFood_list = oldFood.asList()
        # distance from food
        food_distance_list = []
        for food in oldFood_list:
            food_distance = manhattan(food, newPosition)
            food_distance_list.append(food_distance)
        total_food = len(food_distance_list)
        if len(food_distance_list):
            closest_food = min(food_distance_list)
        if closest_food != 0:
            score += 10 / closest_food - total_food
        # distance from ghost
        newGhostStates = successorGameState.getGhostStates()
        ghost_position = []
        for ghost_state in newGhostStates:
            ghost_position.append(ghost_state.getPosition())
        ghost_distance = []
        for position in ghost_position:
            distance = manhattan(position, newPosition)
            ghost_distance.append(distance)
        closest_distance = min(ghost_distance)

        if closest_distance < 3:
            score -= 20
        return score
        # return own score , positive for closeness to food, negative for closeness to ghost

class MinimaxAgent(MultiAgentSearchAgent):
    """
    A minimax agent.

    Here are some method calls that might be useful when implementing minimax.

    `pacai.core.gamestate.AbstractGameState.getNumAgents()`:
    Get the total number of agents in the game

    `pacai.core.gamestate.AbstractGameState.getLegalActions`:
    Returns a list of legal actions for an agent.
    Pacman is always at index 0, and ghosts are >= 1.

    `pacai.core.gamestate.AbstractGameState.generateSuccessor`:
    Get the successor game state after an agent takes an action.

    `pacai.core.directions.Directions.STOP`:
    The stop direction, which is always legal, but you may not want to include in your search.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):

        # get list of actions for initial pacman state and remove "stop" from it
        legal_actions = gameState.getLegalActions(0)
        # define the intiial maximum value and its corresponding best action
        maximum_value = -9999999
        best_action = "Stop"
        depth = self.getTreeDepth()
        legal_actions.remove("Stop")

        # iterate through each action to traverse the search tree
        for action in legal_actions:
            # generate following state through actions
            successor_state = gameState.generateSuccessor(0, action)
            # find max value of successor state through calling the maxvalue function
            value = self.maxvalue(successor_state, depth)
            # if value is greater than initial maximum value, redefine maximum value and best action
            if value > maximum_value:
                maximum_value = value
                best_action = action
        # returns the best action which corresponds to the maximum value
        return best_action

    def maxvalue(self, gameState, depth):
        # check if leaf node, if so, calculate and return value
        if depth == self.getTreeDepth():
            return self.getEvaluationFunction()(gameState)
        # define initial maximum value and find list of actions for pacman gamestate
        maximum_value = -9999999
        legal_actions = gameState.getLegalActions(0)
        # iterate through list of actions while finding the corresponding successor states
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(0, action)
            # find maximum value of state by calling minvalue on succesor state (ghost agent)
            maximum_value = max(maximum_value, self.minvalue(successor_state, 1, depth))

        # returns the highest maximum_value
        return maximum_value

    def minvalue(self, gameState, index, depth):

        # check if leaf node, if so, calculate and return value
        if depth == self.getTreeDepth():
            return self.getEvaluationFunction()(gameState)
        # define initial maximum value and find list of actions for ghost gamestate
        minimum_value = 9999999
        legal_actions = gameState.getLegalActions(index)
        # for ghost #1
        if index < (gameState.getNumAgents() - 1):
            # iterate through list of actions while finding the corresponding successor states
            for action in legal_actions:
                successor_state = gameState.generateSuccessor(index, action)
                # find minimum value of state by calling minvalue on successor state (ghost #2)
                minimum_value = min(minimum_value, self.minvalue(successor_state, index + 1, depth))
        # for ghost #2
        else:
            # iterate through list of actions while finding the corresponding successor states
            for action in legal_actions:
                successor_state = gameState.generateSuccessor(index, action)
                # find minimum value of state by calling maxvalue on successor state (pacman)
                minimum_value = min(minimum_value, self.maxvalue(successor_state, depth + 1))

        # returns the lowest minimum_value
        return minimum_value


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    A minimax agent with alpha-beta pruning.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the minimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):
        legal_actions = gameState.getLegalActions(0)
        # maximizer
        alpha = -9999999
        # minimizer
        beta = 9999999
        v = -9999999
        best_action = "Stop"
        depth = self.getTreeDepth()
        legal_actions.remove("Stop")
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(0, action)
            value = self.maxvalue(successor_state, depth, alpha, beta)
            if value > v:
                v = value
                best_action = action
        return best_action

    def maxvalue(self, gameState, depth, alpha, beta):
        # include win or lose, if depth == 0 (change from self.getTreeDepth())
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.getEvaluationFunction()(gameState)
        v = -9999999
        legal_actions = gameState.getLegalActions(0)
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(0, action)
            tmin = self.minvalue(successor_state, 1, depth, alpha, beta)
            v = max(v, tmin)
            if v > beta:
                # beta = v
                return v
            alpha = max(alpha, v)
        return v

    def minvalue(self, gameState, index, depth, alpha, beta):
        # win or lose, depth = 0
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.getEvaluationFunction()(gameState)
        v = 9999999
        legal_actions = gameState.getLegalActions(index)
        for action in legal_actions:
            if index < (gameState.getNumAgents() - 1):
                successor_state = gameState.generateSuccessor(index, action)
                tmin = self.minvalue(successor_state, index + 1, depth, alpha, beta)
                v = min(v, tmin)
            else:
                successor_state = gameState.generateSuccessor(index, action)
                # changed minus
                tmax = self.maxvalue(successor_state, depth - 1, alpha, beta)
                v = min(v, tmax)
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    An expectimax agent.

    All ghosts should be modeled as choosing uniformly at random from their legal moves.

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`:
    Returns the expectimax action from the current gameState using
    `pacai.agents.search.multiagent.MultiAgentSearchAgent.getTreeDepth`
    and `pacai.agents.search.multiagent.MultiAgentSearchAgent.getEvaluationFunction`.
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)

    def getAction(self, gameState):

        legal_actions = gameState.getLegalActions(0)
        maximum_value = -9999999
        best_action = "Stop"
        depth = self.getTreeDepth()
        legal_actions.remove("Stop")

        for action in legal_actions:
            successor_state = gameState.generateSuccessor(0, action)
            value = self.maxvalue(successor_state, depth)
            if value > maximum_value:
                maximum_value = value
                best_action = action
        return best_action

    def maxvalue(self, gameState, depth):
        if depth == self.getTreeDepth():
            return self.getEvaluationFunction()(gameState)
        maximum_value = -9999999
        legal_actions = gameState.getLegalActions(0)
        for action in legal_actions:
            successor_state = gameState.generateSuccessor(0, action)
            maximum_value = max(maximum_value, self.minvalue(successor_state, 1, depth))
        return maximum_value

    def minvalue(self, gameState, index, depth):

        if depth == self.getTreeDepth():
            return self.getEvaluationFunction()(gameState)
        minimum_values_list = []
        legal_actions = gameState.getLegalActions(index)
        minimum_value = 9999999

        if index < (gameState.getNumAgents() - 1):
            for action in legal_actions:
                successor_state = gameState.generateSuccessor(index, action)
                minimum_value = min(minimum_value, self.minvalue(successor_state, index + 1, depth))
                minimum_values_list.append(minimum_value)
        else:
            for action in legal_actions:
                successor_state = gameState.generateSuccessor(index, action)
                minimum_value = min(minimum_value, self.maxvalue(successor_state, depth + 1))
                minimum_values_list.append(minimum_value)

        num_actions = len(gameState.getLegalActions(index))
        return sum(minimum_values_list) / num_actions


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable evaluation function.

    DESCRIPTION: <write something here so we know what you did>
    """

    return currentGameState.getScore()

class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest.

    You can use any method you want and search to any depth you want.
    Just remember that the mini-contest is timed, so you have to trade off speed and computation.

    Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
    just make a beeline straight towards Pacman (or away if they're scared!)

    Method to Implement:

    `pacai.agents.base.BaseAgent.getAction`
    """

    def __init__(self, index, **kwargs):
        super().__init__(index, **kwargs)
