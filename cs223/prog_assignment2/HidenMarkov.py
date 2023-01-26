from math import *
from hmm import *
class HidenMarkov:

    #A 
    statesSet = {'S1', 'S2', 'S3'}
    
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

    def __init__(self, input_seq):
        self.input_seq = input_seq
    
    def print_dptable(self,V):
        print ("    ")
        for i in range(len(V)): 
            print ("%7s" % i)
        print

        for y in V[0].keys():
            print ("%.5s: " % y)
            for t in range(len(V)):
                print ("%.7s" % ("%f" % V[t][y]))
            print

    def viterbi(self,obs, states, start_p, trans_p, emit_p):
        path = [''] * len(obs)
        prob = -sys.maxsize

        for start_state in start_p:
        	if start_p.get(start_state) > prob:
        		prob = start_p.get(start_state)
        		path[0] = start_state
        
        for i in range(0, len(obs)-1):
        	new_probs = {}
        	for state in states:
        		state_prob = trans_p[path[i]][state] * emit_p[state][obs[i+1]]
        		new_probs[state] = state_prob
        	prob *= min(new_probs.values())
        	path[i+1] = min(new_probs, key=new_probs.get)

        return prob, path

if __name__ == '__main__':
    input_seq = None
    with open("hmm_input_seq.txt") as f:
        input_seq = f.readline().strip()
        print()
        print("HMM input sequence: ", input_seq)
        hm = HidenMarkov(input_seq)
        prob, path = hm.viterbi(input_seq, hm.statesSet,hm.start_probability,hm.trans_probability,hm.emit_propability)
        print("The most probable hidden path sequence that produced the observed sequence",input_seq,"is path:",path,"with Log2(Prob) =",prob)

