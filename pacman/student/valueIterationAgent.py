from pacai.agents.learning.value import ValueEstimationAgent
from collections import Counter

class ValueIterationAgent(ValueEstimationAgent):
    """
    A value iteration agent.

    Make sure to read `pacai.agents.learning` before working on this class.

    A `ValueIterationAgent` takes a `pacai.core.mdp.MarkovDecisionProcess` on initialization,
    and runs value iteration for a given number of iterations using the supplied discount factor.

    Some useful mdp methods you will use:
    `pacai.core.mdp.MarkovDecisionProcess.getStates`,
    `pacai.core.mdp.MarkovDecisionProcess.getPossibleActions`,
    `pacai.core.mdp.MarkovDecisionProcess.getTransitionStatesAndProbs`,
    `pacai.core.mdp.MarkovDecisionProcess.getReward`.

    Additional methods to implement:

    `pacai.agents.learning.value.ValueEstimationAgent.getQValue`:
    The q-value of the state action pair (after the indicated number of value iteration passes).
    Note that value iteration does not necessarily create this quantity,
    and you may have to derive it on the fly.

    `pacai.agents.learning.value.ValueEstimationAgent.getPolicy`:
    The policy is the best action in the given state
    according to the values computed by value iteration.
    You may break ties any way you see fit.
    Note that if there are no legal actions, which is the case at the terminal state,
    you should return None.
    """

    def __init__(self, index, mdp, discountRate = 0.9, iters = 100, **kwargs):
        super().__init__(index, **kwargs)
        self.mdp = mdp
        self.discountRate = discountRate
        self.iters = iters
        # use Counter to intialize dictionaries and set all keys to 0
        self.values = Counter()
        self.policy = Counter()
        self.qvalues = Counter()

        # run loop for each iteration
        for i in range(self.iters):
            states = self.mdp.getStates()
            # copy the current values of the state for the value iteration equation
            prev_values = self.values.copy()
            for state in states:
                # if state is terminal, set policy to None and move to next state
                actions = self.mdp.getPossibleActions(state)
                if len(actions) == 0:
                    continue
                best_action = None
                vvalues = []
                # calculate q value for each action
                for action in actions:
                    q_value = 0
                    # add to q value for each transition probability
                    for (nextstate, prob) in self.mdp.getTransitionStatesAndProbs(state, action):
                        next_reward = mdp.getReward(state, action, nextstate)
                        discount = self.discountRate
                        q_value += prob * (next_reward + prev_values[nextstate] * discount)
                    # store q value in qvalue dictionary
                    self.qvalues[(state, action)] = q_value
                    # find best action for state
                    if self.qvalues[(state, action)] > self.qvalues[(state, best_action)]:
                        best_action = action
                    # append q_value to list  of vvalues
                    vvalues.append(q_value)
                # find max q_value in list
                self.values[state] = max(vvalues)
                # return best action from the state
                self.policy[state] = best_action

        # raise NotImplementedError()

    def getValue(self, state):
        """
        Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def getAction(self, state):
        """
        Returns the policy at the state (no exploration).
        """
        return self.getPolicy(state)

    def getQValue(self, state, action):
        return self.qvalues[(state, action)]

    def getPolicy(self, state):
        return self.policy[state]

'''
I got some assistance from online with value iteration
Title: pacmanreinforcement
Author: Tin Franovic
Date: 2/21
URL: https://bitbucket.org/tfranovic/ai-pacmanreinforcement/src/master/
'''
