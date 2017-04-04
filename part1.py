#!/usr/bin/env python

import better_exceptions

'''
Author(s):
Keith Murray

Contact:
kmurrayis@gmail.com

This is a collection of code that follows Dan Gusfield's work in his book,
"Algorithms, on Strings, Trees, and Sequences"

'''

def testStuff(funcToTest):
    '''
    String Matching Test Cases
    Parameters
    ----------
    funcToTest: Function object

    Returns
    -------
    Nothing, just prints responses


    Notes
    -----
    This should test a number of cases a string matching algorithm 
	might fail at

    '''
    
 
    # Standard Test
    P = "AG"
    T = "GAGACATAGA"
    matches = funcToTest(P, T)
    assert matches == [1, 7],\
        "Expected:\t[1, 7]\nRecieved:\t\t\t" + str(matches)

    # Lots of matches
    P = 'AAA'
    T = 'AAAAAAAAAAA'
    matches = funcToTest(P, T)
    assert matches == [0, 1, 2, 3, 4, 5, 6, 7, 8],\
        "Expected:\t[0, 1, 2, 3, 4, 5, 6, 7, 8]\nRecieved:\t\t\t" + str(matches)


    # Only match is at the end
    P = "A"
    T = "BBBBBBA"
    matches = funcToTest(P, T)
    assert matches == [6],\
        "Expected:\t[6]\nRecieved:\t\t\t" + str(matches)

    # Only match is at the start
    P = "A"
    T = "ABBBBBB"
    matches = funcToTest(P, T)
    assert matches == [0],\
        "Expected:\t[0]\nRecieved:\t\t\t" + str(matches)

    # Match at start and end
    P = "A"
    T = "ABBBBBBA"
    matches = funcToTest(P, T)
    assert matches == [0, 7],\
        "Expected:\t[0, 7]\nRecieved:\t\t\t" + str(matches)


    # Identical strings
    P = "AAAA"
    T = "AAAA"
    matches = funcToTest(P, T)
    assert matches == [0],\
        "Expected:\t[0]\nRecieved:\t\t\t" + str(matches)

    # No Matches
    P = "C"
    T = "ABBBBBBA"
    matches = funcToTest(P, T)
    assert matches == [],\
        "Expected:\t[]\nRecieved:\t\t\t" + str(matches)

    return 


def ch1pt1(P, T):
    '''
    1.1 The Naive Method
    pg 5

    Parameters
    ----------

    P: str
	Pattern of interest
    T: str
	Text being searched Through

    Returns
    -------
    Matches: list
	matching index of starting location of matches


    Notes
    -----
    Method is :math:`Theta`(mn) in time complexity 
	where	n = len(P)
		m = len(T)

    '''

    matches = []
    assert len(T) >= len(P)

    comparisons = 0
    print len(T), len(P)

    for i in range(len(T)-len(P)+1):
	j = 0
	while j < len(P):
	    comparisons += 1
	    if T[i+j] != P[j]:
		# This might be technically a speedup of the naive method. But oh well
		break
	    j += 1
	if j == len(P):
	    matches.append(i)


	#for j in range(len(P)):
	    #if
    print "Actions: ", comparisons, '\n'

    return matches



# A part of 1.3
def ZsubiOfS(S, i):
    assert i > 0
    i = i-1
    for j in range(len(S[i:])):
	if S[j] != S[i+j]:
	    break
    #print j
    return j
    
	
def Z_Algorithm(S):
    '''
    1.4 The Z Algorithm
    pg 9

    Parameters
    ----------

    S: str
	String to preprocess

    Returns
    -------
    Matches: list
	matching index of starting location of matches of length = len(S)


    Notes
    -----
    I don't yet know how to return the Z values...


    '''
    Z = [len(S)] # could be 0 as well, sorta depends on how you want to define 
                # a prefix match of the first character
                # I choose to treat it as a prefix of itself
                # 0 will be slightly more optimized
    r = 0
    l = 0
    #print len(S)
    #counter = 0
    k = 1
    #while k < len(S):
    for k in range(1, len(S)):
	#print k, l, r
	#counter += 1
	if k > r:
	    '''
	    if k>r, then find Zk by explicityly comparing the characters starting at 
	    position k to the characters starting at position 0 of S, until a mismatch is found. 
	    the length of the match is Zk. If Zk > 0, then set r to k+Zk-1, and set l to k
	    ...Adjust in code for zero, not one, indexing..
	    '''
	    # Zk(S)
            zk = 0
            while zk < len(S[k:]):
                #counter += 1
                if S[zk] != S[k+zk]:
		    break
                zk+=1
            '''
	    for zk in range(len(S[k:])):
		counter +=1
		if S[zk] != S[k+zk]:
		    break  # oddly enough, I am almost wishing I had ;'s like in c right
            '''
	    if zk > 0:
		r = k+zk # -1 Text says to subtract 1, but it's 1 indexed, so I think I'm good
		l = k
	else:#elif k <= r: # Should be an else statement, not sure it'll always work, using explicit k<=r
	    '''
	    if k<= r, then positiion k is contained in a zbox, and hence, S(k) is contained in 
	    substring S[l:r]. (alpha)
	    such that l>1, and alpha matches prefix S. Therefore, character S(k) also appears 
	    in position k' = k-l + 1 (or not plus one.. zero indexing?) of S. By the same reasoning,
	    substring S[k:r] (call it beta) must match substring S[k':Zl]. It follows that the 
	    substring beginning at position k must match the prefix of S of length at least the 
	    minimum of Zk' and |beta|, (which is r-k+1) (again, zero index adjustment...)

	    there are two subcases
	    '''
	    kprime = k-l # Man I'm bad with my left and right.... like worse than I should be..
	    lenOfBeta = r-k # I don't think I actually need S[k:r] since it's defined eariler in the string
	    
	    if Z[kprime] < lenOfBeta:
		# then Zk = Zk', and r, l remain unchanged
		zk = Z[kprime]
                #counter += 1
	    else:#elif Z[kprime] >= lenOfBeta:
		'''
		then the enitre substring S[k:r] must be a prefix of S, and Zk>= |beta| = r-k+1. 
		However, Zk might be strictly larger that |beta|, so compare the characters starting
		at position r+1 of S to the characters starting a position |beta|+1 of S until a
		mismatch occurs. Say the mismatch occurs at character q>= r+1. ThenZk is set to
		q-k, r is set to q-1, and l is set to k  

		'''
                q = r
                while q < len(S):
		    #counter += 1
		    if S[q] != S[lenOfBeta-r+q]:
			#print S[q], S[lenOfBeta-r+q]
			break
                    q+=1
                '''
		for q in range( len(S)):
		    counter += 1
		    #print S[l:r]
		    if S[q] != S[lenOfBeta-r+q]:
			#print S[q], S[lenOfBeta-r+q]
			break
                '''
		zk = q-k
		r = q
		l = k

	Z.append(zk)
    #print "counter: ", counter
    return Z


def useZalgorithm(P, T):
    '''
    1.5 The Siimplest linear time exact matching algorithm
    pg 5

    Parameters
    ----------

    P: str
	Pattern of interest
    T: str
	Text being searched Through

    Returns
    -------
    Matches: list
	matching index of starting location of matches


    Notes
    -----
    Method is :math:`Theta`(m+n) in time complexity 
	where	n = len(P)
		m = len(T)
    '''

    S = P + "$" + T
    Zreturn = Z_Algorithm(S)
    matchLen = len(P)
    
    matches = []
    for i in range(len(T)):
	if Zreturn[matchLen + 1 + i] == matchLen:
	    matches.append(i)

    return matches

def ch1pt3(P, T):
    # Not actually worrying about T atm
    #S = P
    S = 'aabcaabxaaz'

    ZsubiOfS(S, 5)
    ZsubiOfS(S, 6)
    ZsubiOfS(S, 7)
    ZsubiOfS(S, 8)
    ZsubiOfS(S, 9)

def ch1pt4():
    S = "caagatxxxxcaagat"
    #    0123456789012345
    T = "gagacatxxxgagacat" # Gagacat unrated ;)
    Z_Algorithm(S)
    Z_Algorithm(T)
    Z_Algorithm("AAAAAAAAAAAAA")
    print Z_Algorithm("AAA$AAAAAAAAA")
    Z_Algorithm("AAAAAAAAAAAAA"*10000)



def Boyer_Moore_Algorithm(P, T):

    return





















#testStuff(ch1pt1)
#ch1pt3("A", "T")
#ch1pt4()
testStuff(useZalgorithm)























