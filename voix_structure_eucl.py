import mido
import pygame
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
from time import time
import gammes2 as gammes
import Algo_rythme_euclidien

class Voix :
    """
    c'est une classe virtuelle
    elle sert de classe mère pour toutes les autres voix
    Si vous avez des changements qui s'appliquent à toutes les voix, veuillez les mettre ici
    """
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo = 120) -> None:
        """
        on initialise toutes les variables
        """

        self.oneTime = 60/tempo
        self.vrtm = vecteur_rythme
        self.l_tab = l_tab
        self.vecteur_init = vecteur_init
        self.output_port = output_port
        self.scale = scale


        # à décider dans les classes
        self.velocity = 64
        # il y a aussi : self.program et self.channel

        #des variables qui vont servir quand on utilisera la voix
        self.i_tab = 0 #position dans la progression d'accord
        self.boolnote= True #indique le besoin de générer une nouvelle note
        self.len_tab = len(l_tab)
        self.v= notes.f_gamme(self.vecteur_init, scale)
        self.debut_bar = time() - 8*self.oneTime
    
    
    def nextTime(self, t = time()):
        """
        Décider de la prochaine note
        """

        if time() >= self.oneTime*8 + self.debut_bar: #début de mesure par la fin de la precedente
           self.changeMesure()
        
        if self.boolnote: #une nouvelle note

            self.t_end = t + self.durationNote()
            self.new_note = self.create_newNote()

            self.boolnote = False
            self.v = notes.f_note(self.v, self.new_note)
            
            return self.new_note
        
        elif time() > self.t_end : #arrêter la note en cours
            note_off = mido.Message("note_off", note = self.new_note, channel = self.channel, velocity = self.velocity)
            self.output_port.send(note_off)

            self.boolnote = True
    


    def changeMesure(self):
        """
        Ici, comprend tout ce qui sera fait quand on change de mesure
        Fonction qui sera appelée par toutes les classes qui héritent de Voix pour en faire leur propore version
        """
        self.root, self.quality, self.seventh = self.l_tab[self.i_tab]
        self.i_tab = (self.i_tab + 1)%self.len_tab
        self.debut_bar += self.oneTime*8
        #print(self.root, self.quality, self.seventh)
    
    def create_newNote(self):
        return main_droite.gen(self.v)

    def durationNote(self):
        """
        En principe jamais appelé, chaque classe héritée utilisera sa propre version de durationNote
        """
        return 0

    def choixInstrument(self):
        """
        Appelée pour chaque voix qui aura son propre instrument, et son canal (channel) de diffusion
        """
        instru = mido.Message("program_change", program = self.program, channel = self.channel)
        self.output_port.send(instru)
    
    def changeTempo(self, tempo):
        self.oneTime = 60/tempo
    
    def stopSound(self):
        note_off = mido.Message("note_off", note = self.new_note, channel = self.channel, velocity = self.velocity)
        self.output_port.send(note_off)
        self.boolnote = True

class VoixGauche (Voix) : 
    
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo)
        
        self.channel = 0
        self.program = 0 #piano


        self.rtm = main_gauche.nouvelle_structure_rythmique(self.vrtm)
        self.i_rtm = 0
        self.len_rtm = len(self.rtm)
        self.l_indices_l = self.init_l_indices_l()
        self.l_notes_l = self.gen_l_notes_l()

        self.choixInstrument()
    
    def init_l_indices_l(self):
        v_l = notes.f_gamme(self.vecteur_init, self.scale)
        root, quality, seventh = self.l_tab[0]
        liste_first_tab = gammes.accord(root, quality, seventh)
        v_l = notes.f_gamme(v_l, gammes.accord(root, quality, seventh))
        liste_notes_l = []
    
        for i in range(0, self.len_rtm):
            new_note_l = main_droite.gen(v_l)
            liste_notes_l.append(new_note_l)

        #la liste des positions des notes dans l'accord
        l_indices_l = notes.search_indices(liste_first_tab, liste_notes_l)
        print(l_indices_l) 
        return l_indices_l
    
    def gen_l_notes_l(self):
        root, quality, seventh = self.l_tab[self.i_tab]
        return gammes.accord(root, quality, seventh)
    
    def changeMesure(self):
        super().changeMesure()
        self.l_notes_l = self.gen_l_notes_l()
        self.v = self.vecteur_init
        self.v = notes.f_gamme(self.v, gammes.accord(self.root, self.quality, self.seventh))

    
    def create_newNote(self):
        new_note_l = self.l_notes_l[self.l_indices_l[self.i_rtm]]
        return new_note_l
    
    def durationNote(self):
        tp_l = self.rtm[self.i_rtm]  #le nombre de temps de la note que l'on va jouer
        self.i_rtm = (self.i_rtm + 1)%self.len_rtm
        return tp_l*self.oneTime

class VoixDroite (Voix) :
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo)

        self.channel = 0
        self.program = 0 #piano

        self.choixInstrument()
    
    def changeMesure(self):
        super().changeMesure()
        self.v = notes.f_newtab(self.v, self.root, self.quality, self.seventh)
    
    def create_newNote(self):
        return super().create_newNote()
    
    def durationNote(self):
        tp = main_droite.gen(self.vrtm)
        t_end = tp*self.oneTime
        return t_end

class VoixEuclideGauche (Voix) : #même objet que voix gauche, mais avec un vecteur de rythme fixe exprimé en bits
    def __init__(self, vecteur_init, vecteur_rythme, l_tab, scale, output_port, nb_actif, nb_tps, offset, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, l_tab, scale, output_port, tempo)
        
        self.channel = 0
        self.program = 0 #piano
        
        self.rtm_eucl = Algo_rythme_euclidien.rythme_euclidien(nb_actif, nb_tps, offset)
        self.i_rtm = 0
        self.len_rtm = len(self.rtm_eucl) #taille du tableau euclidien
        self.l_indices_l = self.init_l_indices_l()
        self.l_notes_l = self.gen_l_notes_l()

        self.choixInstrument()
        
        self.t_end = time()
        
        print(self.rtm_eucl, self.l_indices_l, self.l_notes_l)
    
    def init_l_indices_l(self):
        v_l = notes.f_gamme(self.vecteur_init, self.scale)
        root, quality, seventh = self.l_tab[0]
        liste_first_tab = gammes.accord(root, quality, seventh)
        v_l = notes.f_gamme(v_l, gammes.accord(root, quality, seventh))
        liste_notes_l = []
    
        for i in range(0, self.len_rtm//4 + 1): #a priori on ira jamais plus loin que 1/4 de la taille de rtm_eucl
            new_note_l = main_droite.gen(v_l)
            liste_notes_l.append(new_note_l)

        #la liste des positions des notes dans l'accord
        l_indices_l = notes.search_indices(liste_first_tab, liste_notes_l)
        print(l_indices_l) 
        return l_indices_l
    
    def gen_l_notes_l(self):
        root, quality, seventh = self.l_tab[self.i_tab]
        return gammes.accord(root, quality, seventh)
    
    def changeMesure(self):
        super().changeMesure()
        self.i_rtm = 0
        self.l_notes_l = self.gen_l_notes_l()
        self.v = self.vecteur_init
        self.v = notes.f_gamme(self.v, gammes.accord(self.root, self.quality, self.seventh))

    def create_newNote(self):
        new_note_l = self.l_notes_l[self.l_indices_l[self.i_rtm]]
        return new_note_l
    
    def avanceNote(self):
        bitnote = self.rtm_eucl[self.i_rtm]  #le bit du temps courant
        self.i_rtm = (self.i_rtm + 1)%self.len_rtm
        self.boolnote = bool(bitnote)
    
    def nextTime(self, t = time()):
        """
        Décider de la prochaine note
        """

        if time() >= self.oneTime*8 + self.debut_bar: #début de mesure par la fin de la precedente
           self.changeMesure()
        
        if self.boolnote: #une nouvelle note
            self.new_note = self.create_newNote()            
            self.boolnote = False #sinon nextime va renvoyer des notes en boucle : on en veut juste une
            return self.new_note

        
        elif time() > self.t_end : #arrêter la note en cours
            note_off = mido.Message("note_off", note = self.new_note, channel = self.channel, velocity = self.velocity)
            self.output_port.send(note_off)
            self.t_end += self.oneTime
            self.avanceNote()
            print(self.i_rtm, self.boolnote)
