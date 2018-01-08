#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:09:47 2017

@author: tnemelk
"""

from cipher import base_cipher

class ASYM(base_cipher):
    
    def __init__(self):
        """Un chiffrement asymétrique se définit par une clé publique et une clé privée. """
        base_cipher.__init__(self)
        self.cle_public = None
        self.cle_prive = None
        
       
    def init_encode(self, txt, is_adr, taille_bloc = None):
        """Toute classe de chiffrement a des attributs spécifiques à initialiser.
        La taille de bloc est donnée en bits."""
        base_cipher.init_encode(self, txt, is_adr, taille_bloc)
        
        
    def init_decode(self, txt, is_adr):
        """Toute classe de chiffrement a des attributs spécifiques à initialiser.
        La taille de bloc est donnée en bits."""
        base_cipher.init_decode(self, txt, is_adr)
    
    
    def save_cle_prive(self, adr = "./.cle_prive"):
        """Fonction  de sauveagarde de la clé privée"""
        f = open(adr, "w")
        f.write(self.cle_prive)
        f.close
    
    
    def load_cle_prive(self, is_adr, txt = "./.cle_publique"):
        """Fonction  de chargement de la clé privée"""
        if is_adr:
            f = open(txt, "r")
            K = f.read()
            f.close
        else:
            K = txt
        self.cle_prive = K

    
    def save_cle_publc(self, adr = "./.cle_publique"):
        """Fonction  de sauvegarde de la clé publique"""
        f = open(adr, "w")
        f.write(self.cle_public)
        f.close

        
    def load_cle_publc(self, is_adr, txt = "./.cle_publique"):
        """Fonction  de chargement de la clé publique"""
        if is_adr:
            f = open(txt, "r")
            K = f.read()
            f.close
        else:
            K = txt
        self.cle_public = K

    
    def formate_cle_prive(self):
        """Fonction à redéfinir qui vient former la string privée utilisable """

        
    def formate_cle_publc(self):
        """Fonction à redéfinir qui vient former la string publique utilisable """

        
    def extract_cle_prive(self):
        """Fonction à redéfinir qui vient extraire la clé à partir de la string cle_privée utilisable """

        
    def extract_cle_publc(self):
        """Fonction à redéfinir qui vient extraire la clé à partir de la string cle_publique utilisable """