#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:09:45 2017

@author: tnemelk
"""

from cipher import base_cipher

class SYM(base_cipher):
    
    
    def __init__(self):
        """Un chiffrement sumétrique se définit par une clé secrète. """
        base_cipher.__init__(self)
        self.cle_secrete = None
        self.cbc = False
        self.vec_init_cbc = 0
        
        
    def init_sym(self, cbc = False, vec_init_cbc = 1):
        """Initialise les attributs propres au chiffrement symétrique """
        self.cbc = cbc
        self.vec_init_cbc = vec_init_cbc
        
        
    def init_encode(self, txt, is_adr, taille_bloc = None, cbc = False, vec_init_cbc = 1):
        """Redéfinition de l'initialisation à l'encodage """
        base_cipher.init_encode(self, txt, is_adr, taille_bloc)
        self.init_sym(cbc, vec_init_cbc)
        
        
    def init_decode(self, txt, is_adr, cbc = False, vec_init_cbc = 1):
        """Redéfinition de l'initialisation au décodage"""
        base_cipher.init_decode(self, txt, is_adr)
        self.init_sym(cbc, vec_init_cbc)
        
        
    def init_cle(self, is_newCle, cle = None):
        """Initialise la clé secrète """
        if is_newCle:
            self.gen_cle()
        else:
            self.extract_cle_secrete()
            
            
    def save_keys(self, adr = "./.cle.txt"):
        """Fonction  de sauveagarde de la clé"""
        f = open(adr,"w")
        f.write(self.cle_secrete)
        f.close()
        
        
    def load_keys(self, is_adr, txt = "./.cle.txt"):
        """Fonction  de chargement de la clé à partir d'un fichier ou d'une chaine de caractère"""
        if is_adr:
            f = open(txt,"r")
            r = f.read()
            f.close()
        else:
            r = txt
        self.cle_secrete = r
    
    
    def formate_cle_secrete(self):
        """Fonction à redéfinir qui vient former la string cle_secrete utilisable 
        On doit donner une valeur à self.cle_secrete"""
        
        
    def extract_cle_secrete(self):
        """Fonction à redéfinir qui vient extraire la clé à partir de la string cle_secrete utilisable """
        
        
    def gen_cle(self):
        """Génère une nouvelle clé. """
        
        
    def encode_txt_ebc(self):
        """Mode de chiffrement ebc. """
        self.cipher = [self.code_bloc(bloc) for bloc in self.plain_txt]
    
    
    def cbc_xor(self, actl, prev):
        """Effectue le xor entre deux blocs de mots, à redéfinir """
        return (actl ^ prev)
    
    
    def encode_txt_cbc(self):
        """Mode de chiffrement cbc, par blocs chainés."""
        c = []
        prev = self.vec_init_cbc
        for bloc in self.plain_txt:
            prev = self.code_bloc(self.cbc_xor(bloc, prev))
            c.append(prev)
        self.cipher = c
        
        
    def encode_txt(self):
        """Chiffrement de plain txt """
        self.encode_txt_cbc() if self.cbc else self.encode_txt_ebc()
        
        
    def decode_txt_ebc(self):
        """Mode de déchiffrement ebc. """
        self.plain_txt = [self.decode_bloc(bloc) for bloc in self.cipher]
    
    
    def decode_txt_cbc(self):
        """Mode de déchiffrement cbc."""
        c = []
        prev = self.vec_init_cbc
        for bloc_cip in self.cipher:
            bloc_clr = self.decode_bloc(bloc_cip)
            bloc_clr = self.cbc_xor(bloc_clr, prev)
            c.append(bloc_clr)
            prev = bloc_cip
        self.plain_txt = c
        
        
    def decode_txt(self):
        self.decode_txt_cbc() if self.cbc else self.decode_txt_ebc()