"""
In this file, you will implement generic search algorithms which are called by Pacman agents.
"""

from pacai.util.stack import Stack
from pacai.util.queue import Queue
from pacai.util.priorityQueue import PriorityQueue


def depthFirstSearch(problem):

    """
    Search the deepest nodes in the search tree first [p 85].

    Your search algorithm needs to return a list of actions that reaches the goal.
    Make sure to implement a graph search algorithm [Fig. 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    ```
    print("Start: %s" % (str(problem.startingState())))
    print("Is the start a goal?: %s" % (problem.isGoal(problem.startingState())))
    print("Start's successors: %s" % (problem.successorStates(problem.startingState())))
    ```
    """

    # *** Your Code Here ***
    # create stack, list for visitied nodes, and start state for search problem
    visited_nodes = []
    fringe = Stack()
    start_state = problem.startingState()
    visited_nodes.append(start_state)
    start_tuple = (start_state, [])
    fringe.push(start_tuple)

    # repeat following till fringe is empty
    while fringe:
        # pop next state in the stack
        current_tuple = fringe.pop()
        current_state = current_tuple[0]
        actions = current_tuple[1]
        # identify if state is goal state and return actions if so
        if problem.isGoal(current_state):
            return actions
        # if not goal state, find successor states and add them to fringe if not visisted
        else:
            successor_states = problem.successorStates(current_state)
            for state in successor_states:
                if state[0] not in visited_nodes:
                    visited_nodes.append(state[0])
                    next_state = state[0]
                    # add actions to the list of actions for the search
                    next_actions = actions + [state[1]]
                    next_tuple = (next_state, next_actions)
                    # push successor state to the stack along with the corresponding action
                    fringe.push(next_tuple)
    raise NotImplementedError()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first. [p 81]
    """

    # *** Your Code Here ***
    # create queue, list for visitied nodes, and start state for search problem
    visited_nodes = []
    fringe = Queue()
    start_state = problem.startingState()
    visited_nodes.append(start_state)
    start_tuple = (start_state, [])
    fringe.push(start_tuple)
    # repeat following till fringe is empty
    while fringe:
        # pop next state in the queue
        current_tuple = fringe.pop()
        current_state = current_tuple[0]
        actions = current_tuple[1]
        # identify if state is goal state and return actions if so
        if problem.isGoal(current_state):
            return actions
        # if not goal state, find successor states and add them to fringe if not visisted
        else:
            successor_states = problem.successorStates(current_state)
            for state in successor_states:
                if state[0] not in visited_nodes:
                    visited_nodes.append(state[0])
                    next_state = state[0]
                    # add actions to the list of actions for the search
                    next_actions = actions + [state[1]]
                    next_tuple = (next_state, next_actions)
                    # push successor state to the queue along with the corresponding action
                    fringe.push(next_tuple)
    raise NotImplementedError()

def uniformCostSearch(problem):

    """
    Search the node of least total cost first.
    """
    # *** Your Code Here ***
    # create priority queue, list for visitied nodes, and start state for search problem
    visited_nodes = []
    fringe = PriorityQueue()
    start_state = problem.startingState()
    visited_nodes.append(start_state)
    start_tuple = (start_state, [], 0)
    fringe.push(start_tuple, 0)
    # repeat following till priority queue is empty
    while fringe:
        # pop next state in the priority queue
        current_tuple = fringe.pop()
        current_state = current_tuple[0]
        actions = current_tuple[1]
        # identify if state is goal state and return actions if so
        if problem.isGoal(current_state):
            return actions
        # if not goal state, find successor states and add them to fringe if not visisted
        else:
            successor_states = problem.successorStates(current_state)
            for state in successor_states:
                if state[0] not in visited_nodes:
                    visited_nodes.append(state[0])
                    next_state = state[0]
                    # add actions to the list of actions for the search
                    next_actions = actions + [state[1]]
                    next_tuple = (next_state, next_actions, problem.actionsCost(next_actions))
                    # push successor state to the queue along with the corresponding cost
                    fringe.push(next_tuple, problem.actionsCost(next_actions))
    raise NotImplementedError()

def aStarSearch(problem, heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # *** Your Code Here ***
    # create priority queue, list for visitied nodes, and start state for search problem
    visited_nodes = []
    fringe = PriorityQueue()
    start_state = problem.startingState()
    visited_nodes.append(start_state)
    start_tuple = (start_state, [], 0)
    fringe.push(start_tuple, 0)
    # repeat following till priority queue is empty
    while fringe:
        # pop next state in the priority queue
        current_tuple = fringe.pop()
        current_state = current_tuple[0]
        actions = current_tuple[1]
        # identify if state is goal state and return actions if so
        if problem.isGoal(current_state):
            return actions
        # if not goal state, find successor states and add them to fringe if not visisted
        else:
            successor_states = problem.successorStates(current_state)
            for state in successor_states:
                if state[0] not in visited_nodes:
                    visited_nodes.append(state[0])
                    # add actions to the list of actions for the search
                    next_actions = actions + [state[1]]
                    # calculate the heauristic for the corresponding state
                    h_value = heuristic(state[0], problem)
                    next_cost = problem.actionsCost(next_actions)
                    next_tuple = (state[0], next_actions, next_cost + h_value)
                    # push successor state to the queue with the corresponding cost + heuristic
                    fringe.push(next_tuple, next_cost + h_value)
    raise NotImplementedError()
