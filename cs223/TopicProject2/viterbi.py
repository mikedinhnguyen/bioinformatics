# -*- coding: utf-8 -*-
"""
NAME: viterbi.py

AUTHOR: Leonard P. Wesley

This module contains example Python code of the
viterbi backtrack algorithm.

Change the variable obs to contain the desired
emitted symbols. Then simply execute this module to the obtain
hidden state predictions.

"""

def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}

    # Run Viterbi when t > 0
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t - 1][states[0]]["prob"] * trans_p[states[0]][st]
            prev_st_selected = states[0]

            for prev_st in states[1:]:
                tr_prob = V[t - 1][prev_st]["prob"] * trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob * emit_p[st][obs[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}


    for line in dptable(V):
        print(line)

    opt = []
    max_prob = 0.0
    previous = None

    # Get most probable state and its backtrack
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st

    opt.append(best_st)
    previous = best_st


    # Follow the backtrack till the first observation
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]

    print ('The predicted sequence of hidden states is\n' + ', '.join(opt) + '\nwith highest probability of %s' % max_prob)


def dptable(V):
    # Print a table of steps from dictionary
    yield " ".join(("%12d" % i) for i in range(len(V)))

    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.7s" % ("%f" % v[state]["prob"]) for v in V)

# The variable  obs  specifies the sequence of emission probabilities
# obs = ["A", "G", "C", "G", "C"]
# states = ["CpG", "NotCpG"]  # Hidden states
# start_p = {"CpG": 0.2, "NotCpG": 0.8}   # Start probabilities
# trans_p = {                             # Hidden state ttransition probabilities
#     "CpG": {"CpG": 0.7, "NotCpG": 0.3},
#     "NotCpG": {"CpG": 0.4, "NotCpG": 0.6},
#     }
# emit_p = {                              # Emission probabilitiesS
#     "CpG": {"A": 0.1, "C": 0.4, "T": 0.1, "G": 0.4},
#     "NotCpG": {"A": 0.4, "C": 0.2, "T": 0.2, "G": 0.2},
#     }

#A 
statesSet = ['S1', 'S2', 'S3']

"""
NOTE:  The probability numbers indicated below are in log2 form.  That is,
the probability number =  2^number so for example 2^-1 = 0.5,  and 
2^-2 = 0.25 ... etc.   The reason for this is that Log2 is used to represent
probabilities so that underflow or overflow is not encounrered.  

If you wish to change the probabilities in the tables below, than simple calculate 
Log2(probability that you want/need).  For example Log2(0.33) = -0.6252,  and 
Log2(0.5) = -1,  and so forth. 
"""

#pi:
start_probability = {'S1': -2, 'S2': -1, 'S3': -2}
#tau:
trans_probability = {'S1': {'S1': -1,  'S2': -1.321928,     'S3': -3.321928},
                     'S2'  : {'S1': -float('Inf'),  'S2': -1.,     'S3': -1.},
                     'S3': {'S1': -1.736966,  'S2': -2.321928,     'S3': -1.}}
#e:
emit_propability = {'S1': {'A': -1.321928,    'C': -1.736966,  'T': -2.321928,  'G': -3.321928},
                    'S2': {'A': -2.,   'C': -2., 'T': -2., 'G': -2.},
                    'S3': {'A': -3.321928,    'C': -2.321928,  'T': -1.736966,  'G': -1.321928}}

obs = ["A", "T", "G", "C", "C", "G"]

# Call the viterbu algorithm
#viterbi(obs, states, start_p, trans_p, emit_p)
viterbi(obs, statesSet,start_probability,trans_probability,emit_propability)

# Make sure this module is executed and not imported
if __name__ != "__main__":
    print("This module (viterbi.py) is intended to be executed and not imported.")
