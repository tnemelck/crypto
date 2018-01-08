#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 09:06:46 2017

@author: tnemelk
"""

import random as rdm
#import fichier
from sym import SYM
    
    
class TF(SYM):
    
    
    def __init__(self, p4 = [2, 3, 0, 1], p8 = [4, 2, 6, 7, 1, 3, 0, 5], 
                 p16 = [14, 15, 6, 11, 2, 8, 7, 10, 4, 5, 9, 0, 13, 1, 12, 3],
                 R = 23, C = 2004413935125273122 ):
        
        """taille bloc = 256 ou 512 ou 1024 """
        """Classe de base de three fish """
        
        SYM.__init__(self)
        
        self.mask64 = 2 ** 64 - 1
        
        self.perm_4 = p4
        self.perm_8 = p8
        self.perm_16 = p16
        self.anti_perm_4, self.anti_perm_8, self.anti_perm_16 = self.calc_antiperm()
        self.R = R
        self.C = C
        
        self.nb_mot = None 
        
        self.cle_raw = None
        self.t1 = None
        self.t2 = None
        self.cle = None

        
    #########Redéfinition de foncitons de classes mères########################
    
    
    def init_cle(self, is_new_cle = True, taille_bloc = 1024):
        """Initialise la clé, dans le cas où il faille la générer
        et dans celui où elle a été récupéré d'un fichier."""
        if is_new_cle:
            self.taille_bloc = taille_bloc // 8
            self.nb_mot = self.taille_bloc//8
            self.gen_cle()
            self.formate_cle_secrete()
        else:
            self.taille_bloc, self.cle_raw, self.t1, self.t2 = self.extract_cle_secrete()
            self.nb_mot = self.taille_bloc//8
            self.cle = self.calc_cle()
           
            
    def init_encode(self, txt, is_adr, taille_bloc = 1024, cbc = False, vec_init_cbc = None):
        """Redéfini l'initialisation d'encodage avec comme particularités les
        paramètres cbc."""
        self.nb_mot = taille_bloc // 8
        vec = vec_init_cbc if vec_init_cbc else [2 ** 64 - 1] * self.nb_mot
        SYM.init_encode(self, txt, is_adr, taille_bloc, cbc, vec)
        
        
    def init_decode(self, txt, is_adr, cbc  = False, vec_init_cbc = None):
        """Initialise le décodage."""
        vec = vec_init_cbc if vec_init_cbc else [2 ** 64 - 1] * self.nb_mot
        SYM.init_decode(self, txt, is_adr, cbc, vec)
    
            
    def unRaw(self, txt_raw):
        """Redéfinition de unRaw, voire la classe mère Cipher_Base"""
        ol = self.decoupe_octet_lst(txt_raw, self.taille_bloc)
        ol2 = [self.decoupe_octet_lst(bloc, 8) for bloc in ol]
        result = []
        for b0 in ol2:
            r = []
            for b1 in b0:
                r.append(self.fusion_octet_lst(b1))
            result.append(r)
        return result
        
    
    def raw (self, txt_unRaw):
        """Redéfinition de raw, voire la classe mère Cipher_Base"""
        result = []
        for b0 in txt_unRaw:
            for b1 in b0:
                result += self.fission_octet_fus(b1, 1, 8)
        return result
    
        
    def gen_cle(self):
        """Fonction qui, sachant la clé non découpé et les deux tweaks, forme 
        le troisième tweak, découpe la clé d'origine, et calcule le jeu de clé 
        qui sera utilisé pour chiffrer."""
        self.cle_raw, self.t1, self.t2 = self.alea_cle()
        self.cle = self.calc_cle()
    
    
    def formate_cle_secrete(self):
        """Fonction qui normalise la clé sous la forme d'une chaine de caractères. """
        K = [self.cle_raw, self.t1, self.t2, self.taille_bloc]
        Ks = list(map(str, K))
        self.cle_secrete = (":".join(Ks))
    
    
    def extract_cle_secrete(self):
        """Fonction qui, à partir de la clé normalisé sous forme de chaine de 
        caractères, extrait la clé primaire, les deux tweaks et la taille des blocs."""
        Ks = self.cle_secrete.split(":")
        [cle_raw, t1, t2, taille] = list(map(int, Ks))
        return (taille, cle_raw, t1, t2)
    
    
    def code_bloc(self, bloc):
        """Fonction qui effectue le processus de chiffrement d'un bloc de mots :
            substitution - permutation - ajout de clé """
        mot = self.ajout_cle(bloc, 0)
        for i in range(1, 76+1):
            mot = self.subs(mot)
            mot = self.perm(mot)
            if (i % 4 == 0): mot = self.ajout_cle(mot, i//4)
        return mot
    
    
    def decode_bloc(self, bloc):
        """Fonction qui décode un bloc de mots chiffrés."""
        for i in range(76, 1-1, -1):
            if (i % 4 == 0): bloc = self.ajout_cle(bloc, int(i/4))
            bloc = self.anti_perm(bloc)
            bloc = self.anti_subs(bloc)
        bloc = self.ajout_cle(bloc, 0)
        return bloc
    
    
    def cbc_xor(self, actl, prev):
        """Effectue le xor entre deux blocs de mots. """
        rslt = []
        for i in range(self.nb_mot):
            rslt.append(actl[i] ^ prev[i])
        return rslt
    
    def pad_plain_txt_raw(self):
        """Pad une liste d'octets pour que sa taille soit multiple de la
        taille des blocs, afin d'obtenir un plain_txt homogène.
        Enregistre le nombre d'octets paddé dans un dernier bloc.
        Passe du plain_txt_rax _orignl au plain_txt_raw utilisable."""
        l, q = len(self.plain_txt_raw_orgnl), self.taille_bloc
        self.nb_oct_pad = (((l // q) + 2) * q) - l
        ol = [0] * self.nb_oct_pad
        self.plain_txt_raw = self.plain_txt_raw_orgnl + ol
        f = self.fission_octet_fus(self.nb_oct_pad, 1, 8)
        self.plain_txt_raw[-8:] = f
            
    def unpad_plain_txt_raw(self):
        """Passe du plain_txt au plain_txt_orgnl. Logiquement, le nombre d'octets
        paddés est enregistré dans le dernier bloc de plain_txt."""
        self.nb_oct_pad = self.plain_txt[-1][-1]
        self.plain_txt_raw_orgnl = self.plain_txt_raw[:-self.nb_oct_pad]
        
    ###########Fonctions propres à Three Fish##################################
    
    
    def alea_cle(self):
        """Fonction qui, en utilisant le module random, ressort un clé aléatoire 
        et les deux tweaks t1 et t2, eux aussi aléatoire."""
        k = rdm.randrange(0, (2 ** (self.taille_bloc * 8)))
        t1, t2 = rdm.randrange(0, 2 ** 64), rdm.randrange(0, 2 ** 64)
        return (k, t1, t2)


    def form_cle(self):
        """Fonction qui découpe la clé générée aléatoirement en mots de 64 bits, 
        soit 8 octets, et qui génère le dernier bloc à partir des autres et de 
        constante C."""
        dcle = self.fission_octet_fus(self.cle_raw, 8, self.nb_mot)
        C = self.C
        for c in dcle:
            C ^= c
        dcle.append(C)
        return dcle
    
    
    def form_tweak(self):
        """"Fonction qui génère le troisième tweak. """
        t3 = self.t1 ^ self.t2
        return t3
    
    
    def calc_cle(self):
        """Fonction qui, à partir de la clé Kd découpé et des trois tweaks, 
        calcule les clés de chaque mot des blocs du message découpé, 
        pour 20 tournées."""
        Kd = self.form_cle()
        T = [self.t1, self.t2, self.form_tweak()]
        N = self.nb_mot
        cle = []
        for i in range(19+1):
            c = [Kd[(i+n) % (N+1)] for n in range(N-3)]
            c.append((Kd[(i+N-3) % (N+1)] + T[i % 3]) & self.mask64)
            c.append((Kd[(i+N-2) % (N+1)] + T[(i+1) % 3]) & self.mask64)
            c.append((Kd[(i+N-1) % (N+1)] + i) & self.mask64)
            cle.append(c)
        return cle 
    
        
    def rot_left(self, val, r_bits):
        """Fonciton qui effectue la rotation binaire vers la gauche d'un entier. """
        return((val << (r_bits%64)) & (2**64-1) | \
        ((val & (2**64-1)) >> (64-(r_bits%64))))
     
        
    def rot_right(self, val, r_bits):
        """Fonciton qui effectue la rotation binaire vers la droite d'un entier. """
        return (((val & (2**64-1)) >> r_bits%64) | \
        (val << (64-(r_bits%64)) & (2**64-1)))
        
    
    def subs_paire(self, m1, m2):
        """Fonction qui effectue le processus de substitution sur une paire de mots. """
        m1r = (m1 + m2) & self.mask64
        m2r = m1r ^ self.rot_left(m2, self.R)
        return [m1r, m2r]
    
    
    def anti_subs_paire(self, m1r, m2r):
        """Fonction qui effectue l'anti-substituion d'une paire de mots. """
        m2d = m1r ^ m2r
        m2 = self.rot_right(m2d, self.R)
        m1 = (m1r - m2) & self.mask64
        return [m1, m2]
    
    
    def subs(self, lst):
        """Fonction qui effectue toutes les substitutions des mots d'un bloc
        de mots."""
        l = int(self.nb_mot / 2)
        result = []
        for i in range(l):
            result += self.subs_paire(lst[2*i], lst[2*i + 1])
        return result
    
    
    def anti_subs(self, lst):
        """Fonciton qui effectue l'anti substitution des mots d'un bloc de mots. """
        l = int(self.nb_mot / 2)
        result = []
        for i in range(l):
            result += self.anti_subs_paire(lst[2*i], lst[2*i + 1])
        return result
    
    
    def gen_perm_mat(self, n):
        """Fonction qui génère une matrice de permutation, si le besoin d'en
        changer se fait sentir. Permutation de mots dans un bloc."""
        r = list(range(n))
        while any([r[i] == i for i in range(n)]): rdm.shuffle(r)
        return r
    
    
    def calc_antiperm(self):
        """Fonction qui calcule les fonctions inverses des fonctions de permutation. """
        r4, r8, r16 = list(range(4)), list(range(8)), list(range(16)) 
        for i,e in enumerate(self.perm_4): r4[e] = i
        for i,e in enumerate(self.perm_8): r8[e] = i
        for i,e in enumerate(self.perm_16): r16[e] = i
        return (r4, r8, r16)    
    
    
    def perm(self, lst_mot):
        """Fonction qui effectue la permutation des mots d'un bloc de mot. """
        if (self.nb_mot == 4) :
            pm = self.perm_4 
        elif (self.nb_mot == 8):
            pm = self.perm_8
        else:
            pm = self.perm_16
        result = [0] * self.nb_mot
        for i in range(self.nb_mot):
            result[i] = lst_mot[pm[i]]
        return result
    
    
    def anti_perm(self, lst_mot):
        """Fonction qui effectue la permutation inverse."""
        if (self.nb_mot == 4) :
            apm = self.anti_perm_4
        elif (self.nb_mot == 8):
            apm = self.anti_perm_8
        else:
            apm = self.anti_perm_16
        result = [0] * self.nb_mot
        for i in range(self.nb_mot):
            result[i] = lst_mot[apm[i]]
        return result
    
    def ajout_cle(self, mot, n_tour):
        """Fonction d'ajout de clé de tournée aux mots d'un bloc de mot. """
        result = []
        K = self.cle[n_tour]
        for i, m in enumerate(mot):
            result.append(m ^ K[i])
        return result
    
    def retire_cle(self, mot, n_tour):
        """Fonction  qui effectue l'inverse de l'ajout de clé à un bloc de mots."""
        result = []
        K = self.cle[n_tour]
        for i, m in enumerate(mot):
            result.append(m ^ K[i])
        return result
            
    
    
    ########Comment encoder et décoder un fichier##############################

        
    """
    1) Créez une instance de la classe TF : tf = TF()
    Initialisez toutes les constantes qu vous voulez
    2) Récupèrer le texte et initialiser les premiers attributs
        A) Il s'agit d'une chaine de caractère s : tf.init_encode(s, False, taille_bloc = 1024, cbc = False, vec_init_cbc = None)
        B) Il s'agit d'un fichier à l'adresse adr : tf.init_encode(adr, True, taille_bloc = 1024, cbc = False, vec_init_cbc = None):
        Le choix de la taille de bloc et de l'encodage cbc est vôtre
    3) Initialiser la clé
            A) Vous ne possédez pas la clé : Initialisation de la clé : tf.init_cle(True)
            B) Vous posssédez la clé
                a) Récupérer la clé
                    i) Il s'agit d'une chaine de caractère s : tf.load_keys(False, s)
                    ii) Il s'agit d'un fichier à l'adresse adr : tf.load_keys(True, adr)
                b) Initialiser la clé : tf.init_cle(False)
    4) unRaw : tf.raw2plain_txt()
    5) Chiffrement : tf.encode_txt()
    6) Raw : tf.cipher2raw()
    7) Sauvegarde de la clé à l'adresse adr_cle : tf.save_keys(adr_cle)
    8) Sauvegarde du fichier chiffré à l'adresse adr_cipher : tf.save_file(True, adr_cipher)
    """
    
    
    def encode_three_fish(self, txt, is_adr_plain_txt, adr_cipher, adr_cle = "./.cle.txt", str_cle = None, is_new_cle = True, taille_bloc = 1024, cbc = False, vec_init_cbc = None):
        """Encode avec three fish. """
        self.init_encode(txt, is_adr_plain_txt, taille_bloc, cbc, vec_init_cbc)
        if is_new_cle:
            self.init_cle(True, taille_bloc)
        else:
            self.load_keys(False, str_cle) if str_cle else self.load_keys(True, adr_cle)
            self.init_cle(False)
        self.init_plain_text()
        self.encode_txt()
        self.cipher2raw()
        self.save_keys(adr_cle)
        self.save_cipher_file(adr_cipher)
        
    
    def decode_three_fish(self, txt, is_adr_cipher, adr_cle, adr_plain_txt, str_cle = None, taille_bloc = 1024, cbc = False, vec_init_cbc = None):
        """Décode avec three fish."""
        self.load_keys(False, str_cle) if str_cle else self.load_keys(True, adr_cle)
        self.init_cle(False, taille_bloc)
        self.init_decode(txt, is_adr_cipher, cbc, vec_init_cbc)
        self.raw2cipher()
        self.decode_txt()
        self.plain_txt2raw()
        self.save_plain_txt_file(adr_plain_txt)
        
    def cle_three_fish(self, adr_cle, taille_bloc):
        """Crée une clé secrète three fish """
        self.init_cle(True, taille_bloc)
        self.save_keys(adr_cle)

        
