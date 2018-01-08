#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 16:57:58 2017

@author: tnemelk
"""

import random as rdm
from threading import Thread, RLock

def getD_rec(d, s=0):
    """Renvoie les entiers d et s tels que pour l'entier E en entrée, pair, 
    E = d * 2 ** s
    Algorithme récursif pour montrer qu'on est pas que de amateurs de boucle."""
    if not d & 1: (d, s) = getD_rec(d>>1, s+1)
    return (d, s)


def getD_loop(d):
    s = 0
    while not d&1 :
        s += 1
        d >>= 1
    return (d,s)


def temoin_Miller(alea, nb_test, d, s):
    """Renvoie True si le nombre alea entrée est certain de ne pas être premier,
    False sinon."""
    x = pow(alea, d, nb_test)
    if (x == 1) or (x == (nb_test-1)): return False
    for i in range(s-1):
        x = pow(x, 2, nb_test)
        if x == (nb_test - 1) : return False
    return True

def Miller_Rabin(nb_test, iteration):
    """Test si un nombre est premier, plus iteration est grand, plus le 
    pourcentage de faux positif est faible."""
    if nb_test == 2: return True
    if not (nb_test & 1): return False
    (d, s) = getD_loop(nb_test - 1)
    for i in range(iteration):
        a = rdm.randrange(2, nb_test-1)
        if temoin_Miller(a, nb_test, d, s): return False
    return True


def Miller_Rabin_full(nb_test, iteration):
    if nb_test == 2: return True
    if not (nb_test & 1): return False
    
    s, d = 0, nb_test - 1
    while not d & 1 :
        s += 1
        d >>= 1
            
    for i in range(iteration):
        a = rdm.randrange(2, nb_test-1)
        x = pow(a, d, nb_test)
        if (x == 1) or (x == (nb_test-1)): continue
        for i in range(s-1):
            x = pow(x, 2, nb_test)
            if x == (nb_test - 1) : break
        else : return False
        
    return True
    
def trouv_prime_MR(nb_bits, iteration = 11, mask=None):
    """ Trouve un entier premier de nb_bits. 11 est un nombre d'itération satisfaisant."""
    test = False
    if (not mask): mask = (1 << nb_bits - 1) | 1
    while not test:
        n = rdm.getrandbits(nb_bits - 1) | mask
        test = Miller_Rabin_full(n, iteration)
    return n

def trouv_safe_prime_MR(nb_bits, iteration=11):
    """Trouve un nombre premier sûr, c'est à dire tel que n = 2p+1
    avec n premier et p premier."""
    test = False
    mask = (1 << nb_bits - 2) | 1
    while not test:
        q = trouv_prime_MR(nb_bits - 1, iteration, mask)
        p = (q << 1) | 1
        test =  Miller_Rabin_full(p, iteration)
    return (p, q)

def gen_of_safeprime(prime, q):
    """Trouve 2 entiers générateurs de l'enseble Zprime
    prime est premier et vaut (2q + 1), q étant premier
    l'ordre de prime est (prime - 1) = 2q
    le nombre de diviseur premier de (prime -1) sont q et 2"""
    test = False
    while not test:
        r = rdm.randrange(2, prime)
        t1, t2 = pow(r, 2, prime), pow(r, q, prime)
        test =  (t1 != 1) and (t2 != 1)
    return r
    
class thread_safe_prime(Thread):
    """Thrad qui trouve un entier sûr , permet parallélisation via les 
    variables globales semaphore_sp et verrou_sp"""
    
    def __init__(self, nb_bits, iteration = 11):
        Thread.__init__(self)
        self.nb_bits = nb_bits
        self.iteration = iteration
    
    def run(self):
        """Se termine quand un entier premier sur p = 2*q+1 a été trouvé
        dans une des instances du thread qui partagent des variables."""
        global semaphore_sp, verrou_sp, P, Q
        test_prime = False
        while (not test_prime) and (semaphore_sp):
            q = trouv_prime_MR(self.nb_bits - 1, self.iteration)
            p = (q << 1) | 1
            test_prime =  Miller_Rabin_full(p, self.iteration)
        with verrou_sp :
            if semaphore_sp :
                (P, Q) = (p,q)
                semaphore_sp = False
    
class thread_generateur(Thread):
    """"Thrad qui trouve un générateur pour l'ensemble Zp, p étant un entier sûr,
    permet parallélisation via les variables globales semaphore_gen et verrou_gen"""""
    
    def __init__(self, p, q):
        Thread.__init__(self)
        self.p = p
        self.q= q
        
    def run(self):
        """Se termine quand un entier générateur a été trouvé
        dans une des instances du thread qui partagent des variables."""
        global semaphore_gen, verrou_gen, R
        test_gen = False
        while (not test_gen) and (semaphore_gen):
            r = rdm.randrange(2, self.p)
            t1, t2 = pow(r, 2, self.p), pow(r, self.q, self.p)
            test_gen =  (t1 != 1) and (t2 != 1)
        with verrou_gen:
            if semaphore_gen:
                R = r
                semaphore_gen = False
    
def safe_prime_multiThread(nb_bits, iteration = 11, nb_thread = 4):
    """Lance la recherche d'un entier premier sûr avec multithreading,
    donc parallélisé."""
    global semaphore_sp, verrou_sp, P, Q
    semaphore_sp, verrou_sp = True, RLock()
    T = [thread_safe_prime(nb_bits, iteration) for i in range(nb_thread)]
    for t in T : t.start()
    for t in T : t.join()
    return (P,Q)

def generator_multiThread(p, q, nb_thread = 4):
    """Lance la recherche d'un entier générateur avec multithreading,
    donc parallélisé."""
    global semaphore_gen, verrou_gen, R
    semaphore_gen, verrou_gen = True, RLock()
    T = [thread_generateur(p, q) for i in range(nb_thread)]
    for t in T : t.start()
    for t in T : t.join()
    return R


def test_premier_sur(p):
    return Miller_Rabin_full(p) and Miller_Rabin_full((p-1)/2)

def test_gen_prem_sur(a, p):
    q = (p-1)/2
    return (pow(a, 2, p) != 1) and (pow(a, q, p) != 1)

    
        