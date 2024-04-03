# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:44:43 2023

@author: karma
"""
import numpy as np
import gammes2 as gammes
n_octaves = 7 #nombre d'octaves

vecteur_courant = np.array(88*[1])

gamme = [0, 5, 36, 37, 38, 87]

def norm(v):
    somme = np.sum(v)
    assert somme != 0, "vecteur nul à normaliser"
    return v/somme

def init_v():
    return norm(np.array(88*[1]))

vecteur_courant = norm(vecteur_courant)

def gtab(centre, q = 0.15):
    """
    Parameters
    ----------
    centre : int entre 0 et 88
        DESCRIPTION.
    q : facteur de qualité ajusté empiriquement à 0.15. Influe sur la volatilité de la musique
        DESCRIPTION. The default is 0.15.

    Returns
    -------
    tableau suivant une répartition gaussienne. A priori à multiplier avec notre vecteur courant

    """
    g = np.array([i for i in range(88)])
    g = np.exp(-((g-centre)**2)/2*q**2)
    return g

def mult_terme_a_terme(a, b):
    assert len(a) == len(b), "les deux listes sont de taille différentes"
    res = a*0
    for i in range(len(a)):
        res[i] = a[i]*b[i]
    return res

def gauss(v, centre, q = 0.15):
    """
    applique un filtre gaussien sur v
    """
    return norm(mult_terme_a_terme(v, gtab(centre, q)))

def inverse(liste_notes):
    res = []
    for i in range(0, 88):
        if (not(i in liste_notes)):
            res.append(i)
    return res
        

def f_prefnotes(v, liste_notes, q = 10):
    """liste_notes est une listes d'int de notes
    q correspond au facteur de proportionnalité augmentant ou diminuant les note sélectionnées
    """
    assert type(q) == int or type(q) == float, "problème d'argument"
    w = np.copy(v)
    print(len(w), max(liste_notes))
    for i in liste_notes:
        w[i] *= q
    return norm(w)
        
def f_newtab(v, root = "A", quality = "Major", seventh = "Dominant", q = 10):
    """f(vecteur_courant, accord, q) utilise prefnotes pour initialiser un nouvel accord"""
    w = f_prefnotes(v, gammes.accord(root, quality, seventh), 3)
    return(w)

def f_gamme(v, gamme_courante = gamme, total = True, q = -100):
    """f_gamme annule les notes qui sont hors gamme, ou les diminue si total == false"""
    notes_interdites = inverse(gamme_courante)
    if not(total):
        return f_prefnotes(v, notes_interdites, q)
    else:
        w = np.copy(v)
        for i in notes_interdites:
            w[i] = 0
    return w

def succ(note, g = gamme):
    curr = g[0]
    i = 0
    while curr <= note:
        i += 1
        curr = g[i]
    return g[i]

def pred(note, g = gamme):
    curr = g[-1]
    i = -1
    while curr >= note:
        i -= 1
        curr = g[i]
    return g[i]    
    
def f_precis(v, liste_notes, liste_proba):
    """change la probablité notes par notes à certaines valeurs
    polymorphisme de liste_notes et liste_probas qui peuvent être un élément"""
    #cas ou on travaille avec une note
    if type(liste_notes) == int and type(liste_proba) == float:
        note = liste_notes
        p = liste_proba
        n = v[note]
        w = ((1-p)/(1-n))*v
        w[note] = p
        return w
    
    #else : cas général avec une liste de notes
    assert len(liste_notes) == len(liste_proba)
    n = 0 #somme des probas des notes à modifier
    for i in liste_notes:
        n += v[i]
    p = 0 #somme de liste_proba
    for i in liste_proba: 
        if i < 0:
            return 1/0
        p += i
    w = ((1-p)/(1-n))*v
    for i in range(0, len(liste_notes)):
        w[liste_notes[i]] = liste_proba[i]
    return w
    
def f_note(v, note):
    w = gauss(v, note)
    w = f_prefnotes(w, [note], 0.2)
    w = f_prefnotes(w, [pred(note), note, succ(note)], 2)
    return w

def search_indices(v, val):
    """renvoie les indices dans v associés aux valeurs. les éléments de val doivent etre dans v sinon exeption"""
    l_indices = []
    len_v = len(v)
    
    corr = {}
    for i in range(len_v):
        corr[v[i]] = i

    for i in val:
        if i not in corr:
            ValueError("des éléments de val ne sont pas dans v")
        l_indices.append(corr[i])

    return l_indices
