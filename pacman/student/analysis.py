"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    I increased the noise from 0.2 to 10. This way, even if the policy returned implies the agent
    should take said action to not cross the bridge. Since the noise is set to such a low value,
    the agent will likely end up in the inntended state and will gravitate towards the end of the
    bridge.
    """

    answerDiscount = 0.9
    answerNoise = 0.002

    return answerDiscount, answerNoise

def question3a():
    # close exit risk cliff
    """
    lowering discount to certain degree would ensure closer exit woul dbe prefered.
    No noise would ensure it ends up in the intended state
    """

    answerDiscount = 0.1
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    # close exit no risk
    """
    lowering discount to certain degree would enusre closer exit would be preffered.
    settng reward to 0 as well as low noise would push agent to take the safer path
    """

    answerDiscount = 0.2
    answerNoise = 0.1
    answerLivingReward = 0.0
    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    # distant exit risking cliff
    """
    Higher discount would ensure that farther exit is still preffered.
    Setting Noise to very low as well as negative reward would push the agent
    to risk the cliff as it would land in intended states and try to lose less points
    as possible
    """

    answerDiscount = 0.9
    answerNoise = 0.02
    answerLivingReward = -1

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    The conditions set initially in question would meet this requirment.
    High discount would cause agent to prefer farther exit and a relatively low
    noise would ensure it doesn't risk the cliff
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    Setting living reward to 10 would ensure agent doesn't reach exit
    as it will try to accumulate as many points as possible
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 10

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    """

    # answerEpsilon = 0.3
    # answerLearningRate = 0.5

    # return answerEpsilon, answerLearningRate
    return NOT_POSSIBLE

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
