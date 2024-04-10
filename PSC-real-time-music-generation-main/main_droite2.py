# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 16:06:36 2024

@author: karma
"""

import notes2 as notes
import numpy as np
from random import random

#ça part sur qualque chose de calme

vecteur_rythme = notes.norm(np.array([2, 4, 1, 3, 1, 0, 0, 0])) #le vecteur de proba des rythmes

vecteur_courant = notes.gauss(notes.init_v(), 50)

suite_accords = [("A", "Minor", ""), ("D", "Minor", ""), ("G", "Major", ""), ("C", "Major", "")]

def gen(liste_probas):
    """on suppose que la somme des probas vaut 1
    retourne un indice de la liste"""
    n = len(liste_probas)
    liste_probas = notes.norm(liste_probas)
    return np.random.choice(n,1, p = liste_probas)[0]

def new_song(v = vecteur_courant, vrtm = vecteur_rythme, l_tab = suite_accords, n_iter = 2):
    pos = 0 #le nombre de temps passés depuis le début de la musique
    i_tab = 0 #position dans la progression d'accord
    tp = 1 #temps écoulé dans la note courante - initialisé à 1 pour avoir une note dès le début
    song = []
    len_tab = len(l_tab)
    while i_tab != len(l_tab)*n_iter: #une boucle ou chaque itération vaut un temps
        
        #on gère le changement d'accord
        if pos%8 == 0: #début de mesure
            root, quality, seventh = l_tab[i_tab%len_tab]
            v = notes.f_newtab(v, root, quality, seventh)
            i_tab += 1
        #on gère l'arrivée d'une nouvelle note
        tp -= 1   
        if tp == 0:
            tp = gen(vrtm) + 1 #la durée de la note que l'on va ajouter
            new_note = gen(v)
            song.append((new_note, tp))
            v = notes.f_note(v, new_note) #la fonction qui modifie v à chaque note

        pos += 1
        
        
    return song
