from math import *
from hmm import *
class HidenMarkov:

    #A 
    statesSet = ['-', '+'] 
    # - is non-CpG, + is CpG
    
    """
    NOTE:  The probability numbers indicated below are in log2 form.  That is,
    the probability number =  2^number so for example 2^-1 = 0.5,  and 
    2^-2 = 0.25 ... etc.   The reason for this is that Log2 is used to represent
    probabilities so that underflow or overflow is not encounrered.  
    
    If you wish to change the probabilities in the tables below, than simple calculate 
    Log2(probability that you want/need).  For example Log2(0.33) = -0.6252,  and 
    Log2(0.5) = -1,  and so forth. 
    """
    
    # transition and emission probabilities pulled from website below
    # https://web.stanford.edu/class/stats366/exs/HMM1.html

    # #pi:
    # start_probability = {'A': -2, 'C': -2, 'G': -2, 'T': -2}
    # #tau:
    # trans_probability = {'A': {'A': -2.473931, 'C': -1.867752, 'G': -1.231075, 'T': -3.058894},
    #                      'C': {'A': -2.547932, 'C': -1.442222, 'G': -1.867752, 'T': -2.411195},
    #                      'G': {'A': -2.634867, 'C': -1.560642, 'G': -1.415037, 'T': -3},
    #                      'T': {'A': -3.662004, 'C': -1.494109, 'G': -1.380822, 'T': -2.45799}}

    # #e:
    # emit_propability = {'A': {'A': -2, 'C': 0,  'G': 0,  'T': 0},
    #                     'C': {'A': 0,  'C': -2, 'G': 0,  'T': 0},
    #                     'G': {'A': 0,  'C': 0,  'G': -2, 'T': 0},
    #                     'T': {'A': 0,  'C': 0,  'G': 0,  'T': -2}}

    #pi:
    start_probability = {'-': -1, '+': -1}
    #tau:
    # trans_probability = {'-': {'-': -0.074001, '+': -4.321928},
    #                      '+': {'-': -3.321928, '+': -0.152003}}
    trans_probability = {'-': {'-': -1, '+': -1},
                         '+': {'-': -1, '+': -1}}

    #e:
    emit_propability = {'-': {'A': -1.888969, 'C': -2.058894, 'T': -1.943416, 'G': -2.120294},
                        '+': {'A': -2.736966, 'C': -1.599462, 'T': -2.643856, 'G': -1.473931}}

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
	    V = [{}]
	    for st in states:
	    	# convert start, emit, and trans out of log 2 into probabilities to work with
	        start_converted = 2**start_p[st]
	        emit_converted = 2**emit_p[st][obs[0]]
	        V[0][st] = {"prob": start_converted * emit_converted, "prev": None}

	    # Run Viterbi when t > 0
	    for t in range(1, len(obs)):
	        V.append({})
	        for st in states:
	            trans_converted = 2**trans_p[states[0]][st]
	            max_tr_prob = V[t - 1][states[0]]["prob"] * trans_converted
	            prev_st_selected = states[0]

	            for prev_st in states[1:]:
	                trans_converted2 = 2**trans_p[prev_st][st]
	                tr_prob = V[t - 1][prev_st]["prob"] * trans_converted2
	                if tr_prob > max_tr_prob:
	                    max_tr_prob = tr_prob
	                    prev_st_selected = prev_st

	            emit_converted2 = 2**emit_p[st][obs[t]]
	            max_prob = max_tr_prob * emit_converted2
	            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}


	    # for line in dptable(V):
	    #     print(line)

	    opt = []
	    max_prob = 0.0
	    previous = None
	    best_st = "-"

	    # Get most probable state and its backtrack
	    for st, data in V[-1].items():
	        if data["prob"] > max_prob:
	        	# convert back to log2 probabilities
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


if __name__ == '__main__':
    input_seq = None
    with open("dna_seq3.txt") as f: # replace file name to open, either dna_seq1.txt, dna_seq2.txt, or dna_seq3.txt
        input_seq = f.readline().strip()
        print()
        print("HMM input sequence: ", input_seq)
        hm = HidenMarkov(input_seq)
        hm.viterbi(input_seq, hm.statesSet,hm.start_probability,hm.trans_probability,hm.emit_propability)
    #   print("The most probable hidden path sequence that produced the observed sequence",input_seq,"is path:",path,"with Log2(Prob) =",prob)

