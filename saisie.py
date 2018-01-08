#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 17:17:51 2018

@author: tnemelk
"""

import generateurDeNombrePremier as gnp
import os


def saisie_int(inf, sup):
    s = input("Choisissez bien. \n")
    try:
        r = int(s)
        assert (r >= inf) and (r <= sup) 
    except (ValueError, AssertionError) as e:
        print("La saisie est incorrecte, vous êtes négligeant, ce n'est pas grave, recommencez.")
        r = saisie_int(inf, sup)
    return r


def saisie_Tbloc():
    s = input("Choisissez judicieusement. \n")
    try:
        r = int(s)
        assert (r == 256) or (r==512) or (r==1024)
    except (ValueError, AssertionError) as e:
        print("Vous n'avez que 3 choix possibles, appliquez vous s'il vous plaît.")
        r = saisie_Tbloc()
    return r


def saisie_oui_non():
    dic = {"oui":1, "non":0}
    s = input("""Veuillez marquer "oui" ou "non" en toute lettre. \n""")
    try:
        r = dic[s]
    except KeyError:
        print("""Mon programmmeur ne m'a pas voulu flexible, ainsi, je suis navrée d'avoir à vous demander
de recommencer.""")
        r = saisie_oui_non()
    return r


def affiche_cle_3f(tf):
    [co, t1, t2, tb] = tf.cle_secrete.split(":")
    print("""La clé originale est """, co, "\n"
          """Les deux tweaks sont :""", t1, "et", t2, "\n"
          """Les blocs mesurent """, tb * 8, "bits")

    
def saisie_adr():
    adr = input("Veuillez rentrer l'adresse de votre fichier. \n")
    try:
        assert os.path.isfile(adr)
    except AssertionError:
        """L'adresse saisie ne renvoie pas à un fichier, et ... je ne sais pas quoi faire,
vous pourriez recommencer ... s'il vous-plaît ?"""
        adr = saisie_adr()
    return adr


def saisie_nBits(nbit):
    lim = (2**nbit)-1
    txt = "Entrez un nombre de" + nbit + ", soit inférieur à," + lim + "\n"
    s = input(txt)
    try:
        r = int(s)
        assert (r <= lim) and (r >= 0)
    except (ValueError, AssertionError) as e:
        print(""" Et non, dommage, recommence maintenant.""")
        r = saisie_nBits(nbit)
    print("\n")
    return r


def saisie_cle_tf():
    print("Choisissez la taille des blocs.")
    t_bloc = saisie_Tbloc()
    print("Entrez la clé originale")
    cr = saisie_nBits(t_bloc)
    print("Entrez le premier tweak")
    t1 = saisie_nBits(64)
    print("Entrez le second tweak")
    t2 = saisie_nBits(64)
    cle = [cr, t1, t2, t_bloc]
    cle = map(str, cle)
    print("\n")
    return ":".join(cle)


def saisie_adr_cle_3f():
    adr = saisie_adr()
    f = open(adr,"r")
    k = f.read()
    f.close()
    try:
        Ks = k.split(":")
        assert (len(Ks) == 4) and (all([k.isdigit() for k in Ks])) and \
            (int(Ks[0]) < 2 ** (8 * int(Ks[3]))) and (int(Ks[1]) < 2**64) and (int(Ks[2]) < 2**64)
    except AssertionError:
        print("""La clé stockée dans le fichier est invalide, essaye encore.""")
        adr = saisie_adr_cle_3f()
    print("\n")
    return adr


def affiche_cle_pblc_cs(cs):
    [p, a1, a2, X, Y, W] = cs.cle_public.split(":")
    print("Le grand nombre premier p vaut", p, "\n"
          "Le premier nombre générateur a1 est", a1, "\n"
          "Le second nombre générateur a2 est", a2, "\n"
          "L'entier X vaut", X, "\n"
          "L'entier Y vaut", Y, "\n"
          "L'entier W vaut", W, "\n")

    
def affiche_cle_prive_cs(cs):
    [p, a1, a2, x1, x2, y1, y2, w]  = cs.cle_prive.split(":")
    print("Le grand nombre premier p vaut", p, "\n"
          "Le premier nombre générateur a1 est", a1, "\n"
          "Le second nombre générateur a2 est", a2, "\n"
          "L'entier x1 vaut", x1, "\n"
          "L'entier x2 vaut", x2, "\n"
          "L'entier y1 vaut", y1, "\n"
          "L'entier y2 vaut", y2, "\n"
          "L'entier w vaut", w, "\n")
    

def saisie_nb_prm_sur():
    snp = input("Veuillez entrer votre nombre premier sûr.\n")
    try:
        np = int(snp)
        assert gnp.test_premier_sur(np)
    except (ValueError, AssertionError) as e:
        print("Mais ... ce n'est pas un nombre premier sûr ! Hop hop hop, on recommence !")
        np = saisie_nb_prm_sur()
    print("\n")
    return np


def saisie_nb_gen(p):
    txt = "Veuillez entrer un nombre générateur a1 de" + str(p) + "\n"
    sg = input(txt)
    try:
        g = int(sg)
        assert gnp.test_gen_prem_sur(g, p)
    except (ValueError, AssertionError) as e:
        print("Pff, c'est pas un nombre générateur ça ! Ça, c'est juste nul.")
        g = saisie_nb_gen(p)
    return g
        

def saisie_entier(e):
    txt = "Entrez votre nombre entier positif " + str(e) + "\n"
    s = input(txt)
    try:
        n = int(s)
        assert n >= 0
    except (ValueError, AssertionError) as e:
        print("Ce n'est pas un nombre entier positif, ah ça non !")
        n = saisie_entier(e)
    return n


def saisie_entier_pos(e):
    txt = "Entrez votre nombre entier positif " + str(e) + "\n"
    s = input(txt)
    try:
        n = int(s)
        assert n > 0
    except (ValueError, AssertionError) as e:
        print("Ce n'est pas un nombre entier positif, ah ça non !")
        n = saisie_entier(e)
    return n


def saisie_cle_pblc_cs():
    p = saisie_nb_prm_sur()
    a1 = saisie_nb_gen() % p
    a2 = saisie_nb_gen() % p
    X = saisie_entier("X") % p
    Y = saisie_entier("Y") % p
    W = saisie_entier("W") % p
    result = [p, a1, a2, X, Y, W]
    result = map(str, result)
    result = ":".join(result)
    return result


def saisie_cle_prive_cs():
    p = saisie_nb_prm_sur()
    a1 = saisie_nb_gen() % p
    a2 = saisie_nb_gen() % p
    x1 = saisie_entier("x1") % p
    y1 = saisie_entier("y1") % p
    x2 = saisie_entier("x2") % p
    y2 = saisie_entier("y2") % p
    w = saisie_entier("w") % p
    result = [p, a1, a2, x1, x2, y1, y2, w]
    result = map(str, result)
    result = ":".join(result)
    return result


def saisie_adr_cle_pblc_cs():
    adr = saisie_adr()
    f = open(adr,"r")
    k = f.read()
    f.close()
    try:
        Ks = k.split(":")
        assert (len(Ks) == 6) and (all([k.isdigit() for k in Ks])) and \
            (gnp.test_premier_sur(Ks[0])) and \
            gnp.test_gen_prem_sur(Ks[1], Ks[0]) and gnp.test_gen_prem_sur(Ks[2], Ks[0])
    except AssertionError:
        print("""La clé stockée dans le fichier est invalide, essaye encore.""")
        adr = saisie_adr_cle_pblc_cs()
    print("\n")
    return adr


def saisie_adr_cle_prive_cs():
    adr = saisie_adr()
    f = open(adr,"r")
    k = f.read()
    f.close()
    try:
        Ks = k.split(":")
        assert (len(Ks) == 8) and (all([k.isdigit() for k in Ks])) and \
            (gnp.test_premier_sur(int(Ks[0]))) and \
            gnp.test_gen_prem_sur(int(Ks[1]), int(Ks[0])) and gnp.test_gen_prem_sur(int(Ks[2]), int(Ks[0]))
    except AssertionError:
        print("""La clé stockée dans le fichier est invalide, essaye encore.""")
        adr = saisie_adr_cle_pblc_cs()
    print("\n")
    return adr