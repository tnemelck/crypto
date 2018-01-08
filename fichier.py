#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:29:13 2017

@author: tnemelk
"""

import binr

def file2octets_lst(adr):
    f = open(adr,"rb")
    r = f.read()
    f.close()
    l = list(r)
    return l


def octets_lst2file(nvl_adr, ol):
    f = open(nvl_adr,"wb")
    bol = bytes(ol)
    f.write(bol)
    f.close()
    
def file2str(adr):
    f = open(adr,"r")
    s = f.read()
    f.close()
    return s

def str2file(s, nvl_adr):
    s = str(s)
    f = open(nvl_adr,"w")
    f.write(s)
    f.close()
    
def str2octets_lst(s):
    s = str(s)
    return list(s.encode("utf-8"))

def octets_lst2str(ol):
    return bytes(ol).decode("utf-8", "ignore")


def octets_lst2bits_lst(ol):
    bsl = [binr.int2binlst(o, 8) for o in ol]
    return bsl


def bits_lst2octets_lst(bsl):
    ol = [binr.binlst2int(bl) for bl in bsl]
    return ol


def bits_lst2bin_lst(bsl):
    bl = []
    for o in bsl:
        bl += o
    return bl


def bin_lst2bits_lst(bl):
    bsl, i = [], 0
    while i < len(bl):
        bsl.append(bl[i : i+8])
        i += 8
    return bsl


def file2bits_lst(adr):
    return octets_lst2bits_lst(file2octets_lst(adr))


def bits_lst2file(adr, bsl):
    return octets_lst2file(adr, bits_lst2octets_lst(bsl))


def file2bin_lst(adr):
    return bits_lst2bin_lst(file2bits_lst(adr))


def bin_lst2file(adr, bl):
    return bits_lst2file(adr, bin_lst2bits_lst(bl))


    