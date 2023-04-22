import numpy as np
from fractions import Fraction

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def convert_to_common_denominator(arr):
    denominators = [Fraction(x).limit_denominator().denominator for x in arr]
    common_denominator = 1
    for d in denominators:
        common_denominator = lcm(common_denominator, d)
    numerators = [int(common_denominator * Fraction(x).limit_denominator()) for x in arr]
    return numerators, common_denominator


def solution(m):
    # the sum of the rows
    row_sum = np.sum(m, axis = 1)
    # index of transient states
    transient_states = row_sum.nonzero()[0]
    # index of absorbing states
    absorbing_states = np.where(row_sum == 0)[0]
    if 0 in absorbing_states:
        return [1 if i == 0 or i == len(absorbing_states) else 0 for i in range(len(absorbing_states) + 1)]
    # compute the intial markov probability
    markov = np.matrix(m, dtype=float)
    for nz in transient_states:
        markov[nz] = (markov[nz]) / (row_sum[nz])
    # construct based on the standard form
    # R => rows transitent cols absorbing
    R = markov[transient_states][:, absorbing_states]
    # Q => rows transient cols transient
    Q = markov[transient_states][:, transient_states]
    # F => fundamental matrix (I - Q)^(-1)
    F = (np.identity(len(transient_states)) - Q)**(-1)
    
    # L => Limiting matrix part
    L = F * R
    
    # the first row is the result we want
    state_zero_row = np.array(L[np.where(transient_states == 0)[0]]).flatten()
    
    # convert based on the requred form by the problem
    numerators, denominator = convert_to_common_denominator(state_zero_row)
    numerators.append(denominator)
    return numerators