#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 22:03:36 2017

@author: tnemelk
"""

import fichier

class base_cipher():
    
    def __init__(self):
        """Les algorithmes de chiffrements prennent un texte_raw qu'elle mettent en forme 
        pour ensuite le chiffrer ou le déchiffer.
        Cette mise en forme passe souvent par la décomposition en bloc, 
        chaque bloc étant composé d'un ou plusieurs octets.
        On différencie le plain text pur/original et celui ayant subi le pad."""
        self.cipher = None
        self.cipher_raw = None
        self.plain_txt_raw = None
        self.plain_txt_raw_orgnl = None
        self.nb_oct_pad = None
        self.plain_txt = None
        self.taille_bloc = 8
        
        
    def get_octet_lst(self, txt, is_adr):
        """Si is_adr == True, alors txt est l'adresse du fichier à récupérer
        Sinon, le text est une chaine de caractère, ou un nombre qui sera convertit en string"""
        if is_adr:
            ol = fichier.file2octets_lst(txt)
        else:
            ol = fichier.str2octets_lst(txt)
        return ol
    
    
    def save_cipher_file(self, adr):
        """Sauvegarde directement le cipher"""
        fichier.octets_lst2file(adr, self.cipher_raw)
        
    def save_plain_txt_file(self, adr):
        """Sauvegarde directement le plain_txt"""
        fichier.octets_lst2file(adr, self.plain_txt_raw_orgnl)
        
    
    
    def save_file(self, iscipher, adr = "./Texte.txt"):
        """Fonction  de sauveagarde d'un fichier chiffré ou déchiffré à une 
        adresse normée : adresseDeBase_cipher ou adresseDeBase_plaintxt"""
        txt = "_cipher" if iscipher else "_plaintxt"
        base = str(adr).split(".")
        base.insert(-1, txt)
        nvl_adr = ".".join(base[:-2]) + ".".join(base[-2:])
        if iscipher:
            fichier.octets_lst2file(nvl_adr, self.cipher_raw)
        else:
            fichier.octets_lst2file(nvl_adr, self.plain_txt_raw_orgnl)
            
            
    def decoupe_octet_lst(self, ol, nb_octet_pBloc):
        """Découpe une liste d'octets en blocs. """
        result = []
        for i in range(0,len(ol), nb_octet_pBloc):
            result.append(ol[i : i + nb_octet_pBloc])
        return result
    
    
    def recolle_lst_octet_lst(self, lol):
        """ Recolle des blocs en liste d'octets"""
        result = []
        for ol in lol: result += ol
        return result
    
    
    def fusion_octet_lst(self, ol):
        """Fusionne les octets d'un bloc en valeur à chiffrer """
        l = len(ol) - 1
        result = sum([o << (8 * (l-i)) for i, o in enumerate(ol)])
        return result
    
    
    def fission_octet_fus(self, of, nb_octet_pMot, nb_mot):
        """Fissionne une valeur chiffrée en bloc d'octets. """
        lst_oct = [(of % ((2 ** (8*nb_octet_pMot*(i))))) >> (8 * nb_octet_pMot * (i-1)) for i in range (nb_mot, 0, -1)]
        return lst_oct
    
    
    def init_encode(self, txt, is_adr, taille_bloc = None):
        """Toute classe de chiffrement a des attributs spécifiques à initialiser.
        La taille de bloc est donnée en bits."""
        self.plain_txt_raw_orgnl = self.get_octet_lst(txt, is_adr)
        if taille_bloc : self.taille_bloc = taille_bloc // 8
        
        
    def init_decode(self, txt, is_adr):
        """Toute classe de chiffrement a des attributs spécifiques à initialiser.
        La taille de bloc est donnée en bits."""
        self.cipher_raw = self.get_octet_lst(txt, is_adr)
        
    
    def code_bloc(self, bloc):
        """Le principe des algorithmes de chiffrements est de chiffrer des blocs de valeurs,
        qui peuvent être un octet ou le regroupement de plusieurs octets.
        Cette fonction est bien entendu à redéfinir pour chaque algo."""
        
        
    def decode_bloc(self, bloc):
        """Le principe des algorithmes de chiffrements est de chiffrer des blocs de valeurs,
        qui peuvent être un octet ou le regroupement de plusieurs octets.
        Cette fonction est bien entendu à redéfinir pour chaque algo."""
        
        
    def encode_txt(self):
        """Encode chaque bloc. """
        self.cipher = [self.code_bloc(bloc) for bloc in self.plain_txt]
        
        
    def decode_txt(self):
        """ Décode chaque bloc"""
        self.plain_txt = [self.decode_bloc(bloc) for bloc in self.cipher]
        
        
    def unRaw(self, txt_raw):
        """Prend une liste d'octets raw et la rend utilisable, à redéfinir """
        
        
    def raw(self, txt_unRaw):
        """Remet un text en format raw """
        
        
    def plain_txt2raw(self):
        """Transforme le plain_text en plain text raw
        et le plain_txt_raw en plain_txt_raw_orgnl"""
        self.plain_txt_raw = self.raw(self.plain_txt)
        self.unpad_plain_txt_raw()
        
        
    def raw2plain_txt(self):
        """Transforme le plain txt raw en plain txt"""
        self.plain_txt = self.unRaw(self.plain_txt_raw)
        
        
    def cipher2raw(self):
        """Transforme le cipher en cipher raw"""
        self.cipher_raw = self.raw(self.cipher)
        
        
    def raw2cipher(self):
        """Tranforme le cipher raw en cipher"""
        self.cipher = self.unRaw(self.cipher_raw)
        
        
    def pad_plain_txt_raw(self):
        """Pad une liste d'octets pour que sa taille soit multiple de la
        taille des blocs, afin d'obtenir un plain_txt homogène.
        Enregistre le nombre d'octets paddé dans un dernier bloc.
        Passe du plain_txt_rax _orignl au plain_txt_raw utilisable."""
        l, q = len(self.plain_txt_raw_orgnl), self.taille_bloc
        self.nb_oct_pad = (((l // q) + 2) * q) - l
        ol = [0] * self.nb_oct_pad
        self.plain_txt_raw = self.plain_txt_raw_orgnl + ol
        f = self.fission_octet_fus(self.nb_oct_pad, 1, self.taille_bloc)
        self.plain_txt_raw[-self.taille_bloc:] = f
            
    def unpad_plain_txt_raw(self):
        """Passe du plain_txt au plain_txt_orgnl. Logiquement, le nombre d'octets
        paddés est enregistré dans le dernier bloc de plain_txt."""
        self.nb_oct_pad = self.plain_txt[-1]
        self.plain_txt_raw_orgnl = self.plain_txt_raw[:-self.nb_oct_pad]
    
    
    def init_plain_text(self):
        """À partir du plain_txt_raw_orgnl, obtient le plain_txt_raw et 
        le plain_txt"""
        self.pad_plain_txt_raw()
        self.raw2plain_txt()
            