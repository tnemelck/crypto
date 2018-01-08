#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 02:18:23 2017

@author: tnemelk
"""

import tkinter as tk

from threeFish import TF
from cramer_shoup import CS
from skein_hash import SH
import fichier
import os


class Info():
    
    
    def __init__(self):
        self.adr_txt_orgn = None
        self.txt_orgn = None
        self.is_adr_txt = None
        self.adr_key = None
        self.txt_key = None
        self.is_adr_key = None
        self.adr_txt_dest = None
        
        

root = tk.Tk()
root.title("Outils de cryptographie sans pareil")

class T_bloc(tk.Frame):
    
    """Fenêtre de selection de taille de bloc """
    
    
    def __init__(self, fenetre, **kwargs):
        tk.Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        
        self.pack(fill=tk.BOTH)
        
        self.val = tk.IntVar(); self.val.set(1024)
        self.txt_tbloc = tk.Label(self, text="Choisir la taille de vos blocs, en bits.")
        self.rb_256 = tk.Radiobutton(self, text = "256",  variable = self.val, value = 256)
        self.rb_712 = tk.Radiobutton(self, text = "712", variable = self.val, value = 712)
        self.rb_1024 = tk.Radiobutton(self, text = "1024", variable = self.val, value = 1024)
        
        self.txt_tbloc.pack(side = tk.TOP)
        self.rb_256.pack(side = tk.LEFT, padx = 5, pady = 20)
        self.rb_712.pack(side = tk.LEFT, padx = 10, pady = 20)
        self.rb_1024.pack(side = tk.LEFT, padx = 15, pady = 20)
        

class Key_sym_selection(tk.Frame):
    def __init__(self, fenetre, **kwargs):
        tk.Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        
        self.pack(fill = tk.BOTH)
        self.val = tk.IntVar() ; self.val.set(1)
        self.key_txt = tk.Label(self, text = "Choisir la clé secrète.")


class Txt_choice(tk.Frame):
    
    global info
    
    def __init__(self, is_cipher, fenetre, **kwargs):
        
        global info
        
        tk.Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        
        self.cpmlt = "déchiffrer." if is_cipher else "chiffrer."
        
        self.pack(fill=tk.BOTH)
        
        self.val = tk.IntVar(); self.val.set(1024)
        self.txt_tbloc = tk.Label(self, text="Choisir le texte à chiffer.")
        self.rb_adr = tk.Radiobutton(self, text = "Adresse du fichier texte à " + self.cpmlt, variable =self.val, value = 0)
        self.rb_plain_txt = tk.Radiobutton(self, text = "Texte à chiffrer.",  variable = self.val, value = 1)
        self.scroll = tk.Scrollbar(self)
        self.entry_plain_txt = tk.Text(self, height = 10, width = 50)
        self.cipher_file = tk.Button(text='Ouvrir', command=self.callback)
        
        self.txt_tbloc.pack(side = tk.TOP)
        self.rb_adr.pack(side = tk.LEFT, padx=5, pady = 5)
        self.cipher_file.pack(side = tk.LEFT, padx=5, pady = 10)
        self.rb_plain_txt.pack(side = tk.LEFT, padx=15, pady =5)
        self.scroll.pack(side = tk.RIGHT)
        self.entry_plain_txt.pack(side = tk.LEFT, padx = 15, pady = 10)
        self.scroll.config(command = self.entry_plain_txt.yview)
        self.entry_plain_txt.config(wrap = tk.WORD, yscrollcommand = self.scroll.set)
        
        
                
    def callback(self):
            global info
            name= tk.filedialog.askopenfilename()
            info.adr_txt_orgn = name    
    


class Adr_txt(tk.Frame):
    
    global info
    
    def __init__(self, v, cplmt, fenetre, **kwargs):
        tk.Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        
        self.rb_adr = tk.Radiobutton(self, text = "Adresse du fichier texte à " + self.cpmlt,  variable =self.val, value = 0)
        self.cipher_file = tk.Button(text='Ouvrir', command=self.callback)
        self.rb_adr.pack(side = tk.TOP)
        self.cipher_file.pack(side = tk.BOTTOM)
        
    
    def callback(self):
            global info
            name= tk.filedialog.askopenfilename()
            info.adr_txt_orgn = name


class Content_txt(tk.Frame):
    global info
    
    def __init__(self, v, cplmt, fenetre, **kwargs):
        tk.Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.rb_adr = tk.Radiobutton(self, text = "Adresse du fichier texte à " + self.cpmlt,  variable =self.val, value = 0)
        self.cipher_file = tk.Button(text='Ouvrir', command=self.callback)
        self.rb_adr.pack(side = tk.TOP)
        self.cipher_file.pack(side = tk.BOTTOM)



#frame_tbloc = T_bloc(root)
frame_txt = Txt_choice(False, root)
root.mainloop()

