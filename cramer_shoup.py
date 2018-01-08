#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 17:32:15 2017

@author: tnemelk
"""

import generateurDeNombrePremier as gnp
import random as rdm
import skein_hash as sh
from asym import ASYM



class CS(ASYM):
    
    def __init__(self, nb_bits_hsh = 1024):
        
        """Comme particularités, nous avons tous les attributs qui formerontc les clés
        et des taille de bloc différente pour le cipher et le plain text.
        L'attribut verif décode sert uniquement si un message n'est pas authentique."""
        
        ASYM.__init__(self)
        
        self.nb_bits_hsh = nb_bits_hsh
        
        self.verif_decode = True
        
        self.taille_bloc_plain_txt = 0
        self.taille_bloc_cipher = 0
        self.p = 0
        self.a1 = 0
        self.a2 = 0
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
        self.w = 0
        self.X = 0
        self.Y = 0
        self.W = 0
        

    def gen_cles(self, iteration, nb_thread, nb_bits = 1024):
        """Génère les 8 entiers qui constituent les clés. """
        p, q = gnp.safe_prime_multiThread(nb_bits, iteration, nb_thread)
        a1, a2 = gnp.generator_multiThread(p, q, nb_thread), gnp.generator_multiThread(p, q, nb_thread)
        while a2 == a1 : a2 = gnp.generator_multiThread(p, q, nb_thread)
        x1 = rdm.randrange(p)
        x2 = rdm.randrange(p)
        y1 = rdm.randrange(p)
        y2 = rdm.randrange(p)
        w = rdm.randrange(p)
        return (p, a1, a2, x1, x2, y1, y2, w)
    
    def calc_cles(self):
        """Calcule les trois entiers nécessaire au décodage avec clé privée. """
        X = (pow(self.a1, self.x1, self.p) * pow(self.a2, self.x2, self.p)) % self.p
        Y = (pow(self.a1, self.y1, self.p) * pow(self.a2, self.y2, self.p)) % self.p
        W = pow(self.a1, self.w, self.p)
        return (X, Y, W)    
    
    
    def calc_taille_bloc(self):
        """Le nombre d'octets concaténés dépend de l'entier p
        ou est choisi par l'utilisateur, en bit.
        Cependant, comme tout est modulo p, il ne faut pas avoir des blocs
        plus grands que p."""
        l = self.p.bit_length()
        if l % 8 == 0:
            tbpt = l // 8 - 1
        else:
            tbpt = l // 8
        tbc = tbpt + 1
        return tbpt, tbc
    
    def init_atrbt_publc(self, p, a1, a2, X, Y, W, ):
        """Initialise les attribut propres à la clé publique."""
        self.p = p
        self.a1 = a1
        self.a2 = a2
        self.X = X
        self.Y = Y
        self.W =W
        self.taille_bloc_plain_txt, self.taille_bloc_cipher = self.calc_taille_bloc()
        self.taille_bloc = self.taille_bloc_plain_txt
        
    def init_atrbt_prive(self, p, a1, a2, x1, x2, y1, y2, w):
        """Initialise et calcule les attribut propres à la clé publique."""
        self.p = p
        self.a1 = a1
        self.a2 = a2
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.w = w
        X, Y, W = self.calc_cles()
        self.X = X
        self.Y = Y
        self.W = W
        self.taille_bloc_plain_txt, self.taille_bloc_cipher = self.calc_taille_bloc()
        self.taille_bloc = self.taille_bloc_plain_txt
    
    
    def init_encode(self, txt, is_adr):
        """Initialise l'encodage ; pas de choix sur la taille des blocs. """
        ASYM.init_encode(self, txt, is_adr, None)
        
        
    def init_decode(self, txt, is_adr):
        """Initialise le décodage
        À noter que l'avoir ici est inutile, mais c'est plus propre."""
        ASYM.init_decode(self, txt, is_adr)
    
    
    def hash_int2str(self, m):
        """Utilise l'agorithme skein de hashage, le hash fait 1024 bits, soit 128 octets et est un entier,
        mais peut aussi faire 256 ou 512 bits.
        On en fait un string pour pouvoir les concaténer ensemble."""
        hc = sh.SH(m, False, self.nb_bits_hsh)
        hsh = hc.hsh()
        return str(hsh)
    
    
    def multiple_hsh(self, *i):
        """Calcule et concatène des hashs, puis hash la concaténation
        Le rend sous la forme d'entier."""
        l = list(i)
        H = [self.hash_int2str(m) for m in l]
        S = "".join(H)
        final_hash = self.hash_int2str(S)
        return int(final_hash)
    
    
    def code_bloc(self, mot):
        """c représente le message, B1 et B2 des entiers pour la vérification et
        v l'entier de vérification."""
        b = rdm.randrange(1, self.p)
        B1, B2 = pow(self.a1, b, self.p), pow(self.a2, b, self.p)
        c = (mot * pow(self.W, b, self.p)) % self.p
        B = self.multiple_hsh(B1, B2, c) % self.p
        v = (pow(self.X, b, self.p) * pow(self.Y, b * B, self.p)) % self.p
        return [B1, B2, c, v]
    
    
    def verif_bloc(self, bloc):
        """Vérifie que le bloc est authentique. """
        (B1, B2, c, v0) = bloc
        B = self.multiple_hsh(B1, B2, c) % self.p
        v = (pow(B1, self.x1, self.p) * pow(B2, self.x2, self.p) * pow((pow(B1, self.y1, self.p) * pow(B2, self.y2, self.p)), B, self.p)) % self.p
        return v == v0
    
    
    def decode_bloc(self, bloc):
        """Décode le bloc. """
        B1, c = bloc[0], bloc[2]
        exp = (self.w * (self.p - 2))
        m = (pow(B1, exp, self.p) * c) % self.p
        return m
    
    
    def encode_txt(self):
        """Redéfini la fonction d'encodage. Est aussi inutile puisque identique
        dans la classe mère de cipher."""
        result = [self.code_bloc(mot) for mot in self.plain_txt]
        self.cipher = result
    
    
    def decode_txt(self):
        """Décode le texte en vérifiant que le message soit authentique. """
        result = []
        for bloc in self.cipher:
            (B1, B2, c, v) = bloc
            if self.verif_bloc(bloc): 
                result.append(self.decode_bloc(bloc))
            else:
                self.plain_txt = [42]
                self.verif_decode = False
                break
        self.plain_txt = result
                
            
    def plain_txt2raw(self):
        """Transforme le plain txt en plain txt raw"""
        ptd = [self.fission_octet_fus(of, 1, self.taille_bloc_plain_txt) for of in self.plain_txt]
        self.plain_txt_raw = self.recolle_lst_octet_lst(ptd)
        self.unpad_plain_txt_raw()
        
        
    def raw2plain_txt(self):
        """Transforme le plain_tex rawt en plain text"""
        ptd = self.decoupe_octet_lst(self.plain_txt_raw, self.taille_bloc_plain_txt)
        self.plain_txt = [self.fusion_octet_lst(ol) for ol in ptd]
        
        
    def cipher2raw(self):
        """Transforme le cipher en cipher raw
        Le cipher est sous la forme de None si le décodage s'est mal passé 
        ou une liste de liste sous la forme [B1, B2, c, v]"""
        cipher_fission = []
        for mot in self.cipher:
            octet_lst = [self.fission_octet_fus(of, 1, self.taille_bloc_cipher) for of in mot]
            cipher_fission += self.recolle_lst_octet_lst(octet_lst)
        self.cipher_raw = cipher_fission
        
        
    def raw2cipher(self):
        """Tranforme le cipher raw en cipher"""
        nb_elmnt = 4
        result = []
        crd = self.decoupe_octet_lst(self.cipher_raw, nb_elmnt * self.taille_bloc_cipher)
        for mot in crd:
            mot_dcp = self.decoupe_octet_lst(mot, self.taille_bloc_cipher)
            mot_fuse = [self.fusion_octet_lst(o) for o in mot_dcp]
            result.append(mot_fuse)
        self.cipher = result
            
    
    def formate_cle_prive(self):
        """Formate la clé privé sous une forme normée. """
        t = [self.p, self.a1, self.a2, self.x1, self.x2, self.y1, self.y2, self.w]
        t = list(map(str, t))
        rslt = ":".join(t)
        self.cle_prive = rslt
        
        
    def extract_cle_prive(self):
        """Récupère les attibuts de la clé privé à partir de sa forme normée."""
        K = self.cle_prive.split(":")
        [p, a1, a2, x1, x2, y1, y2, w] = list(map(int, K))
        return (p, a1, a2, x1, x2, y1, y2, w)
        
    
    def formate_cle_publc(self):
        """Formate la clé publique sous une forme normée. """
        t = [self.p, self.a1, self.a2, self.X, self.Y, self.W]
        t = list(map(str, t))
        rslt = ":".join(t)
        self.cle_public = rslt
    
    
    def extract_cle_publc(self):
        """Récupère les attibuts de la clé publique à partir de sa forme normée."""
        K = self.cle_public.split(":")
        [p, a1, a2, X, Y, W] = list(map(int, K))
        return (p, a1, a2, X, Y, W)
    
    
    def init_cle_publc(self):
        (p, a1, a2, X, Y, W) = self.extract_cle_publc()
        self.init_atrbt_publc(p, a1, a2, X, Y, W)
        
    def init_cle_prive_use(self):
        (p, a1, a2, x1, x2, y1, y2, w) = self.extract_cle_prive()
        self.init_atrbt_prive(p, a1, a2, x1, x2, y1, y2, w)
        
    def init_cle_prive_new(self, nb_bits_cle, iteration, nb_thread):
        (p, a1, a2, x1, x2, y1, y2, w) = self.gen_cles(iteration, nb_thread, nb_bits_cle)
        self.init_atrbt_prive(p, a1, a2, x1, x2, y1, y2, w)
    
    
    def encode_cramer_shoup(self, is_adr_plain_text, txt_plain_txt, is_adr_cle, txt_cle = "./.cle_pblc.txt",  adr_cipher = "./cipher_text.txt"):
        """Encode avec Cramer Shoup. """
        self.init_encode(txt_plain_txt, is_adr_plain_text)
        self.load_cle_publc(is_adr_cle, txt_cle)
        self.init_cle_publc()
        self.init_plain_text()
        self.encode_txt()
        self.cipher2raw()
        self.save_cipher_file(adr_cipher)
    
    
    def decode_cramer_shoup(self, is_adr_cipher, txt_cipher, is_adr_cle, txt_cle = "./.cle_pblc.txt",  adr_plain_txt = "./plainTxt_text.txt"):
        """Décode avec Cramer Shoup."""
        self.init_decode(txt_cipher, is_adr_cipher)
        self.load_cle_prive(is_adr_cle, txt_cle)
        self.init_cle_prive_use()
        self.raw2cipher()
        self.decode_txt()
        self.plain_txt2raw()
        self.save_plain_txt_file(adr_plain_txt)
        
    def cle_cramer_shoup(self, adr_cle_publc, adr_cle_prive, nb_bits_cle = 1024, iteration = 11, nb_thread = 8):
        """Calcul des clés façon Cramer-Shoup."""
        self.init_cle_prive_new(nb_bits_cle, iteration, nb_thread)
        self.formate_cle_prive()
        self.formate_cle_publc()
        self.save_cle_prive(adr_cle_prive)
        self.save_cle_publc(adr_cle_publc)
        
        
        
        
