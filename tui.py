#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 16:57:20 2018

@author: tnemelk
"""


from threeFish import TF
from cramer_shoup import CS
from skein_hash import SH
import fichier
import sys
import saisie

        
def accueil():
    print("""Bienvenue dans l'interface texte d'un outil de cryptographie sans pareil.
Plusieurs choix vous sont proposés :
          Si vous souhaitez quitter ce superbe programme, tapez 0.
          Si vous souhaitez générer une clé de chiffrement Three Fish, tapez 1.
          Si vous souhaitez chiffrer un message avec l'algorithme Three Fish, tapez 2.
          Si vous sohaitez déchiffrer un message avec l'algorithme Three Fish, tapez 3.
          Si vous souhaitez générer une clé de chiffrement Cramer-Shoup, tapez 4.
          Si vous souhaitez chiffrer un message avec l'algorithme Cramer-Shoup, tapez 5.
          Si vous sohaitez déchiffrer un message avec l'algorithme Cramer-Shoup, tapez 6.
          Enfin, si vous souhaitez hasher un message avec l'algorithme de hashage Skain hash, tapez 7.""")
    r = saisie.saisie_int(0, 7)
    if r == 0:
        sys.exit()
    elif r == 1:
        cle_3f()
    elif r == 2:
        chfr_3f()
    elif r == 3:
        dchfr_3f()
    elif r == 4:
        cle_cs()
    elif r == 5:
        chfr_cs()
    elif r == 6:
        dchfr_cs()
    elif r == 7:
        hsh()
    sys.exit()
    
        
def cle_3f(tf = None):
    print("""Il vous faut choisir la taille de vos blocs.
Vous avez le choix entre 256, 512 et 1024.""")
    t_bloc = saisie.saisie_Tbloc()
    if not tf: tf = TF()
    tf.init_cle(taille_bloc=t_bloc)
    print("""\nVoulez-vous afficher la clé générée ?""")
    rep = saisie.saisie_oui_non()
    if rep : saisie.affiche_cle_3f(tf)
    print("""\nVoulez vous enregistrer cette clé dans un fichier ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
        tf.save_keys(adr)
    print("\nFélicitations, vous avez généré une clé avec Three Fish.\n\n")
    accueil()
    sys.exit()

    
def chfr_3f():
    tf = TF()
    print("""\nSi vous préférez chiffrer un fichier, tapez 1.
Si vous préférez plutôt chiffrer un texte saisi, tapez 2.""")
    is_adr_file = (saisie.saisie_int(1, 2) == 1)
    pt = saisie.saisie_adr() if is_adr_file else input("""Veuillez rentrer le texte à chiffrer.\n""")
    print("""\nVoulez vous utiliser le mode de chiffrement cbc ? Un non implique le mode ebc.""")
    is_cbc = saisie.saisie_oui_non()
    tf.init_encode(pt, is_adr_file, cbc=is_cbc)
    print("""\nSi vous préférez entrez l'adresse de la clé secrète, tapez 1.
Si vous préférez plutôt la saisir à la main, tapez 2.
Enfin, si vous voulez en générer une nouvelle, tapez 3.""")
    rep = saisie.saisie_int(1, 3)
    if (rep == 1) or (rep == 2):
        if rep == 1:
            adr_cle = saisie.saisie_adr_cle_3f()
            tf.load_keys(True, adr_cle)
        else:
            cle = saisie.saisie_cle_tf()
            tf.load_keys(False, cle)
        tf.init_cle(False)
        if rep == 2 :
            print("""Voulez vous enregistrer cette clé dans un fichier ?""")
            rep = saisie.saisie_oui_non()
            if rep:
                adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
                tf.save_keys(adr)
    else:
        tf = cle_3f(tf)
    tf.init_plain_text()
    tf.encode_txt()
    tf.cipher2raw()
    print("""Voulez vous lire le message chiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep : print(fichier.octets_lst2str(tf.cipher_raw))
    print("""\nVoulez vous sauvegarder le message chiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
        tf.save_cipher_file(adr)
    print("\nFélicitations, vous avez chiffré un message avec Three Fish.\n\n")
    accueil()
    sys.exit()


def dchfr_3f():
    tf = TF()
    print("""\nSi vous préférez déchiffrer un fichier, tapez 1.
Si vous préférez plutôt déchiffrer un texte saisi, tapez 2.""")
    is_adr_file = (saisie.saisie_int(1, 2) == 1)
    ct = saisie.saisie_adr() if is_adr_file else input("""Veuillez rentrer le texte à chiffrer.\n""")
    print("""Voulez vous utiliser le mode de déchiffrement cbc ? Un non implique le mode ebc.""")
    is_cbc = saisie.saisie_oui_non()
    print("""Si vous préférez entrez l'adresse de la clé secrète, tapez 1.
Si vous préférez plutôt la saisir à la main, tapez 2.\n""")
    rep = saisie.saisie_int(1, 2)
    if rep == 1:
        adr_cle = saisie.saisie_adr_cle_3f()
        tf.load_keys(True, adr_cle)
    else:
        cle = saisie.saisie_cle_tf()
        tf.load_keys(False, cle)
    tf.init_cle(False)
    if rep == 2 :
        print("""Voulez vous enregistrer cette clé dans un fichier ?""")
        rep = saisie.saisie_oui_non()
        if rep:
            adr = input("Veuillez rentrer l'adresse où enregistrer le fichier.\n")
            tf.save_keys(adr)
    tf.init_decode(ct, is_adr_file, is_cbc)
    tf.raw2cipher()
    tf.decode_txt()
    tf.plain_txt2raw()
    print("""Voulez vous lire le message déchiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep : print(fichier.octets_lst2str(tf.plain_txt_raw_orgnl))
    print("""Voulez vous sauvegarder le message déchiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier.\n")
        tf.save_plain_txt_file(adr)
    print("Félicitations, vous avez déchiffré un message avec Three Fish.")
    accueil()
    sys.exit()

    
def hsh():
    
    print("""\nSi vous préférez hasher un fichier, tapez 1.
Si vous préférez plutôt haser un texte saisi, tapez 2.""")
    is_adr = (saisie.saisie_int(1, 2) == 1)
    txt = saisie.saisie_adr() if is_adr else input("""Veuillez rentrer le texte à hasher. \n""")
    print("""\nIl vous faut choisir la taille de vos blocs.
Vous avez le choix entre 256, 512 et 1024.""")
    tbloc = saisie.saisie_Tbloc()
    h = SH(txt, is_adr, taille_bloc=tbloc)
    H = h.hsh()
    print("""Voulez vous lire le hash ?""")
    rep = saisie.saisie_oui_non()
    if rep : print("\n", H)
    print("""\nVoulez vous enregistrer ce hash dans un fichier ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
        h.save_hsh(adr)
    print("""\nFélicitations, vous avez hasher un message avec Skein hash.\n\n\n""")
    accueil()
    sys.exit()
    
    
def chfr_cs():
    cs = CS()
    print("""\nSi vous préférez chiffrer un fichier, tapez 1.
Si vous préférez plutôt chiffrer un texte saisi, tapez 2.""")
    is_adr_file = (saisie.saisie_int(1, 2) == 1)
    pt = saisie.saisie_adr() if is_adr_file else input("""Veuillez rentrer le texte à chiffrer.\n""")
    cs.init_encode(pt, is_adr_file)
    print("""\nSi vous préférez entrez l'adresse de la clé secrète, tapez 1.
Si vous préférez plutôt la saisir à la main, tapez 2.""")
    rep = saisie.saisie_int(1, 2)
    if rep == 1:
        adr_cle = saisie.saisie_adr_cle_pblc_cs()
        cs.load_keys(True, adr_cle)
    else:
        cle = saisie.saisie_cle_pblc_cs()
        cs.load_keys(False, cle)
    cs.init_cle_publc()
    if rep == 2 :
        print("""Voulez vous enregistrer cette clé dans un fichier ?""")
        rep = saisie.saisie_oui_non()
        if rep:
            adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
            cs.save_cle_publc(adr)
    cs.init_plain_text()
    cs.encode_txt()
    cs.cipher2raw()
    print("""Voulez vous lire le message chiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep : print(fichier.octets_lst2str(cs.cipher_raw))
    print("""\nVoulez vous sauvegarder le message chiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
        cs.save_cipher_file(adr)
    print("\nFélicitations, vous avez chiffré un message avec Cramer-Shoup.\n\n")
    accueil()
    sys.exit()
    
def dchfr_cs():
    cs = CS()
    print("""\nSi vous préférez déchiffrer un fichier, tapez 1.
Si vous préférez plutôt déchiffrer un texte saisi, tapez 2.""")
    is_adr_file = (saisie.saisie_int(1, 2) == 1)
    ct = saisie.saisie_adr() if is_adr_file else input("""Veuillez rentrer le texte à chiffrer.\n""")
    print("""Si vous préférez entrez l'adresse de la clé secrète, tapez 1.
Si vous préférez plutôt la saisir à la main, tapez 2.\n""")
    rep = saisie.saisie_int(1, 2)
    if rep == 1:
        adr_cle = saisie.saisie_adr_cle_prive_cs()
        cs.load_cle_prive(True, adr_cle)
    else:
        cle = saisie.saisie_cle_prive_cs()
        cs.load_keys(False, cle)
    cs.init_cle()
    if rep == 2 :
        print("""Voulez vous enregistrer cette clé dans un fichier ?""")
        rep = saisie.saisie_oui_non()
        if rep:
            adr = input("Veuillez rentrer l'adresse où enregistrer le fichier.\n")
            cs.save_cle_prive(adr)
    cs.init_decode(ct, is_adr_file)
    cs.raw2cipher()
    cs.decode_txt()
    cs.plain_txt2raw()
    print("""Voulez vous lire le message déchiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep : print(fichier.octets_lst2str(cs.plain_txt_raw_orgnl))
    print("""Voulez vous sauvegarder le message déchiffré ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier.\n")
        cs.save_plain_txt_file(adr)
    print("Félicitations, vous avez déchiffré un message avec Cramer Shoup.")
    accueil()
    sys.exit()
    
def cle_cs():
    cs = CS()
    nb_bits_cle = saisie.saisie_entier_pos("qui sera la taille de votre nombre premier sûr, en bit.")
    nb_threads = saisie.saisie_entier_pos("qui sera le nombre de thread mis en place pour calculer le nombre premier.")
    nb_iter = saisie.saisie_entier_pos("qui sera le nombre d'itération utilisés par l'algorithme de Miller Rabin." )
    cs.init_cle_prive_new(nb_bits_cle, nb_iter, nb_threads)
    cs.formate_cle_prive()
    cs.formate_cle_publc()
    print("""\nVoulez-vous afficher la clé publique générée ?""")
    rep = saisie.saisie_oui_non()
    if rep : saisie.affiche_cle_pblc_cs(cs)
    print("""\nVoulez-vous afficher la clé privée générée ?""")
    rep = saisie.saisie_oui_non()
    if rep : saisie.affiche_cle_prive_cs(cs)
    print("""\nVoulez vous enregistrer la clé publique dans un fichier ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
        cs.save_cle_publc(adr)
    print("""\nVoulez vous enregistrer la clé privée dans un fichier ?""")
    rep = saisie.saisie_oui_non()
    if rep:
        adr = input("Veuillez rentrer l'adresse où enregistrer le fichier. \n")
        cs.save_cle_prive(adr)
    print("\nFélicitations, vous avez généré une clé avec Cramer-Shoup. \n\n")
    accueil()
    sys.exit()
    
accueil()



    
