#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:48:55 2017

@author: tnemelk
"""

def int2binstr(n):
    return bin(n)[2:]

def binstr2binlst(s, taille = False):
    l = list(s)
    result = list(map(int, l))
    if taille != False : result = pad(result, taille)
    return result

def int2binlst(n, taille = False):
    return binstr2binlst(int2binstr(n), taille)


def binstr2int(s):
    return int(s, 2)

def binlst2binstr(l):
    ls = map(str, l)
    s = "".join(ls)
    return s

def binlst2int(l):
    return binstr2int(binlst2binstr(l))

def pad(l, width, content = 0):
    d = width - len(l)
    if d < 0:
        C = l[-width:]
    elif d > 0:
        C = ([content] * d) + l
    else:
        C = l
    return C

def double_pad(L1, L2, width = False, content = 0):
    l1, l2 = len(L1), len(L2)
    lm = max(l1, l2)
    if width == False:
        P1 = pad(L1, lm, content)
        P2 = pad(L2, lm, content)
    else:
        P1 = pad(L1, width, content)
        P2 = pad(L2, width, content)
    return (P1, P2)
        

def xor_binlst(a, b):
    #a et b des listes de char 0 ou 1
    A, B = double_pad(a, b)
    X = []
    for i in range(len(A)):
        x = 0 if (A[i] == B[i]) else 1
        X.append(x)
    return X

def xor_blocs(b1, b2):
    if len(b1) != len(b2) : 
        print("Nombre d'octets par bloc irrégulier")
        exit
    b = []
    for i in len(b1):
        b.append(xor_binlst(b1[i], b2[i]))
    return b
    

def or_binlst(a, b):
    A, B = double_pad(a, b)
    X = []
    for i in range(len(A)):
        x = 1 if (A[i] == 1) or (B[i] == 1) else 0
        X.append(x)
    return X

def and_binlst(a, b):
    A, B = double_pad(a, b)
    X = []
    for i in range(len(A)):
        x = 1 if (A[i] == 1) and (B[i] == 1) else 0
        X.append(x)
    return X

def ind_bin(bl, reverse = False):
    if reverse : bl = reversed(bl)
    ind = [i for i,e in enumerate(bl) if e == 1]
    return ind

def inv_bin(lst):
    return list(map(lambda x: 1-x, lst))

def add_sans_ret(a, b, lim = False):
    A, B = double_pad(a, b, lim)
    A, B = list(reversed(A)), list(reversed(B))
    r = 0
    S = []
    for i in range(len(A)):
        s = A[i] + B[i] + r
        s, r = s % 2, int(s >= 2)
        S.append(s)
    return list(reversed(S))

def sous_sans_ret(a, b, lim = False):
    A, B = double_pad(a, b, lim)
    Br = inv_bin(B)
    Bm = add_sans_ret(Br, [1])
    s = add_sans_ret(A, Bm)
    return s
    

def dec_g(lb):
    lb.append(lb[0])
    lb = lb[1:]
    return lb

def dec_d(lb):
    lb.insert(0, lb[-1])
    lb = lb[:-1]
    return lb
    
def dec(lb, n, droite = False):
    if droite:
        for i in range(n):
            lb = dec_d(lb)
    else:
        for i in range(n):
            lb = dec_g(lb)
    return lb
    
