#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 11:54:36 2017

@author: tnemelk
"""

from threeFish import TF
import fichier

class SH(TF):
    
    def __init__(self, txt, is_adr, taille_bloc = 1024, p4 = [2, 3, 0, 1], p8 = [4, 2, 6, 7, 1, 3, 0, 5], 
                 p16 = [14, 15, 6, 11, 2, 8, 7, 10, 4, 5, 9, 0, 13, 1, 12, 3],
                 R = 23, C = 2004413935125273122, cle_depart =  14159265358979323846264338327950288419716939937510582097494459230781640628620):
        
        """taille bloc = 256 ou 512 ou 1024 
        Hash produit égal à cette taille de bloc
        Si is_adr == True, on récupère la hash du fichier
        Sinon, le txt est converti directement."""
        
        """"Héritage"""
        TF.__init__(self, p4, p8, p16, R, C)
        
        """Attributs propres à la séquence entrée"""
        self.init_encode(txt, is_adr, taille_bloc, False, None)
        self.nb_mot = self.taille_bloc // 8
        self.init_plain_text()
        
        """ Attributs propre à three fish, constantes """
        self.mask64dec = self.mask64 << 64
        self.mask128 = 2 ** 128 - 1
        self.cle_depart = cle_depart
        
        """Attributs propres à UBI
        On redéfinit le tweak comme 
        0-125 : Nombre d'octets traités incluant en cours = Position
        126 : Position Premier octet = debut
        127 : Position Dernier octet = final"""
        self.debut = self.taille_bloc
        self.final = (len(self.plain_txt) - 1) * self.taille_bloc
        self.position = 0
        
        """Attributs de fin, le fameux hash """
        self.hash = 0
        
    
    def init_hash(self):
        """Réinitianyle les paramètres de hash """
        self.cle_raw = self.cle_depart
        self.debut = self.taille_bloc
        self.final = (len(self.plain_txt) - 1) * self.taille_bloc
        self.position = 0
        
    
    def gen_tweak(self):
        """"FOnction qui génère les 2 tweaks. """
        T = self.position + ((self.debut == self.position) << 126) + ((self.position == self.final) << 127)
        self.t1 = T & self.mask64
        self.t2 = (T & self.mask64dec) >> 64     
        
        
    def gen_cle(self):
        """Fonction qui, sachant la clé non découpé et les deux tweaks, forme 
        le troisième tweak, découpe la clé d'origine, et calcule le jeu de clé 
        qui sera utilisé pour chiffrer."""
        self.gen_tweak()
        self.cle = self.calc_cle()
    
    
    def reform_cle(self, cle):
        """Remet une clé sous forme d'entier """
        rc = 0
        for i, c in enumerate(reversed(cle)):
            rc += c << (64 * i)
        return rc
    
    
    def inc_pos(self):
        """Incrément le champ position"""
        self.position += self.taille_bloc
        
        
    def hsh(self):
        """Génère le hash"""
        self.init_hash()
        for bloc in self.plain_txt:
            self.inc_pos()
            self.gen_cle()
            self.cle_raw = self.reform_cle(self.cbc_xor(self.code_bloc(bloc) , bloc))
        self.hash = self.cle_raw
        return self.hash
    
    def save_hsh(self, adr):
        """Sauvegarde le hash """
        fichier.str2file(self.hash, adr)
    
        
            
    
    
        

