# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 00:57:44 2023

@author: karma

8 temps par mesure

objectif : créer une main gauche

pour ça : on commence par créer une structure rythmique
"""
from random import random
import numpy as np
import notes2 as notes
import gammes2 as gammes

p_rtm = np.array([0.2, 0.4, 0.15, 0.2, 0.05, 0, 0, 0]) #le vecteur de probabilité des rythmes

l_tab = [("A", "Minor", ""), ("D", "Minor", ""), ("G", "Major", ""), ("C", "Major", "")]

def gen(liste_probas):
    """on suppose que la somme des probas vaut 1
    retourne un indice de la liste"""
    n = len(liste_probas)
    liste_probas = notes.norm(liste_probas)
    return np.random.choice(n,1, p = liste_probas)[0]

def nouvelle_structure_rythmique(probas_rythmes = p_rtm):
    liste_rythmes = []
    somme = 0
    while somme <=8:
        r = gen(probas_rythmes) +1
        liste_rythmes.append(r)
        somme += r
    liste_rythmes.pop()
    liste_rythmes.append(r + 8 - somme)
    return liste_rythmes


def vecteur_accompagnement(notes_accord, q = 0.13):
    """prend en argument les notes de l'accord (et un facteur de qualité pour la gaussienne)
    rend un vecteur de proba avec uniquement les notes de l'accord"""
    v = notes.init_v()
    v = notes.f_gamme(v, notes_accord) #on retire les notes hors accord
    v = notes.gauss(v, 30, q)
    return v
    
def acc_monortm(liste_accords = l_tab):
    """prend en argument une liste d'accords et renvoie un accompagnement sous la forme
    d'une liste de (int note, int temps en 8/8)
    la structure rythmique est aléatoire mais identique pour chaque mesure
    les notes sont choisies dans l'accord et en gaussienne"""
    rythmes = nouvelle_structure_rythmique()
    n = len(rythmes)
    liste_sons = []
    for tab in liste_accords:
        root, quality, seventh = tab
        v = vecteur_accompagnement(gammes.accord(root, quality, seventh)) #on transforme le tab en listes de notes int
        for i in range(n):
            liste_sons.append((gen(v), rythmes[i]))
    return liste_sons
        

    

    
    
    
