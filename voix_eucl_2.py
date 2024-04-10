import mido
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
from time import time
import gammes2 as gammes
import Algo_rythme_euclidien
import random as rd
import boucle_accords

class Voix :
    """
    c'est une classe virtuelle
    elle sert de classe mère pour toutes les autres voix
    Si vous avez des changements qui s'appliquent à toutes les voix, veuillez les mettre ici
    """
    def __init__(self, vecteur_init, vecteur_rythme, scale, output_port, tempo = 120, proba_faux = 0.01) -> None:
        """
        on initialise toutes les variables
        """
        #initialisation des variables de bases
        self.oneTime = 60/tempo
        self.vrtm = vecteur_rythme
        self.vecteur_init = vecteur_init
        self.output_port = output_port
        self.scale = scale
        self.proba_faux = proba_faux

        self.t_end = time()

        # à décider dans les classes
        self.velocity = 64
        # il y a aussi : self.program et self.channel

        #des variables qui vont servir quand on utilisera la voix
        self.boolnote= True #indique le besoin de générer une nouvelle note
        self.v= notes.f_gamme(self.vecteur_init, scale)
        self.debut_bar = time() - 8*self.oneTime

    def init_later(self):
        pass
    
    def nextTime(self, t = time()):
        """
        Décider de la prochaine note
        """

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
    
    def stopSound(self):
        print("Stopping")
        for i in range(128):
            note_off = mido.Message("note_off", note = i, channel = self.channel, velocity = self.velocity)
            self.output_port.send(note_off)
        self.boolnote = True

    def changeMesure(self):
        """
        Ici, comprend tout ce qui sera fait quand on change de mesure
        Fonction qui sera appelée par toutes les classes qui héritent de Voix pour en faire leur propore version
        """
        pass
    
    def changeParamMesure(self, root, quality):
        self.root = root
        self.quality = quality

    def create_newNote(self):
        decalage = rd.choices([-1,0,1], weights=[self.proba_faux/2, 1-self.proba_faux, self.proba_faux/2], k=1)[0]
        return main_droite.gen(self.v) + decalage

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
    
    def parent_orchestre(self, orch):
        self.parent = orch
    
    def get_info_orchestre(self):
        self.seventh = self.parent.get_seventh()
        self.root = self.parent.get_root()
        self.quality = self.parent.get_quality()
    
    def changeTempo(self, tempo):
        self.oneTime = 60/tempo
    

class VoixGauche (Voix) : 
    
    def __init__(self, vecteur_init, vecteur_rythme, scale, output_port, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, scale, output_port, tempo)
        
        self.channel = 0
        self.program = 0 #piano


        self.rtm = main_gauche.nouvelle_structure_rythmique(self.vrtm)

        self.choixInstrument()
    
    def init_later(self):
        self.i_rtm = 0
        self.len_rtm = len(self.rtm)
        self.l_indices_l = self.init_l_indices_l()
        self.l_notes_l = self.gen_l_notes_l()

    def init_l_indices_l(self):
        v_l = notes.f_gamme(self.vecteur_init, self.scale)
        liste_first_tab = gammes.accord(self.root, self.quality, self.seventh)
        v_l = notes.f_gamme(v_l, gammes.accord(self.root, self.quality, self.seventh))
        liste_notes_l = []
    
        for i in range(0, self.len_rtm):
            new_note_l = main_droite.gen(v_l)
            liste_notes_l.append(new_note_l)

        #la liste des positions des notes dans l'accord
        l_indices_l = notes.search_indices(liste_first_tab, liste_notes_l)
        print(l_indices_l) 
        return l_indices_l
    
    def gen_l_notes_l(self):
        return gammes.accord(self.root, self.quality, self.seventh)
    
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
    def __init__(self, vecteur_init, vecteur_rythme, scale, output_port, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, scale, output_port, tempo)

        self.channel = 10
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
    def __init__(self, vecteur_init, vecteur_rythme, scale, output_port, nb_actif, nb_tps, offset, tempo=120) -> None:
        super().__init__(vecteur_init, vecteur_rythme, scale, output_port, tempo)
        
        self.channel = 0
        self.program = 0 #piano
        
        self.rtm_eucl = Algo_rythme_euclidien.rythme_euclidien(nb_actif, nb_tps, offset)
        print(self.rtm_eucl)
        
        self.choixInstrument()
    
    def init_later(self):
        self.i_rtm = 0
        self.len_rtm = len(self.rtm_eucl) #taille du tableau euclidien
        self.l_indices_l = self.init_l_indices_l()
        self.l_notes_l = self.gen_l_notes_l()
        print(self.l_indices_l)


    def init_l_indices_l(self):
        v_l = notes.f_gamme(self.vecteur_init, self.scale)
        liste_first_tab = gammes.accord(self.root, self.quality, self.seventh)
        v_l = notes.f_gamme(v_l, gammes.accord(self.root, self.quality, self.seventh))
        liste_notes_l = []
    
        for i in range(0, self.len_rtm//4 + 1): #a priori on ira jamais plus loin que 1/4 de la taille de rtm_eucl
            new_note_l = main_droite.gen(v_l)
            liste_notes_l.append(new_note_l)

        #la liste des positions des notes dans l'accord
        l_indices_l = notes.search_indices(liste_first_tab, liste_notes_l)
        return l_indices_l
    
    def gen_l_notes_l(self):
        return gammes.accord(self.root, self.quality, self.seventh)
    
    def changeMesure(self):
        super().changeMesure()
        self.i_rtm = 0
        self.l_notes_l = self.gen_l_notes_l()
        self.v = self.vecteur_init
        self.v = notes.f_gamme(self.v, gammes.accord(self.root, self.quality, self.seventh))

    def create_newNote(self):
        if self.i_rtm>len(self.l_indices_l)-1:
            print("erreur")
        new_note_l = self.l_notes_l[self.l_indices_l[self.i_rtm]]
        return new_note_l
    
    def avanceNote(self):
        bitnote = self.rtm_eucl[self.i_rtm]  #le nombre de temps de la note que l'on va jouer
        self.i_rtm = (self.i_rtm + 1)%len(self.l_indices_l)
        self.boolnote = bool(bitnote)
    
    def nextTime(self, t = time()):
        """
        Décider de la prochaine note
        """
        
        if self.boolnote: #une nouvelle note
            self.new_note = self.create_newNote()            
            self.boolnote = False #sinon nextime va renvoyer des notes en boucle : on en veut juste une
            return self.new_note

        
        elif time() > self.t_end : #arrêter la note en cours
            note_off = mido.Message("note_off", note = self.new_note, channel = self.channel, velocity = self.velocity)
            self.output_port.send(note_off)
            self.t_end += self.oneTime
            self.avanceNote()


class Orchestre :
    def __init__(self, tonic_init, quality_init, gamme_init, tab_voix) -> None:
        self.tonic_init = tonic_init
        self.quality_init = quality_init
        self.gamme_init = gamme_init
        self.tab_voix = tab_voix

        self.oneTime = tab_voix[0].oneTime
        self.debut_bar = time() - 8*self.oneTime

        self.root, self.quality = self.gamme_init
        self.seventh = "Dominant"
        self.i_changement_acc = 1 #position dans la progression d'accord

        for voix in self.tab_voix:
            voix.parent_orchestre(self)
            voix.get_info_orchestre()
            voix.init_later()


        self.to_play = []
    
    def nextTime(self, t = time()):
        for voix in self.tab_voix:
            note = voix.nextTime(t)
            if note:
                self.to_play.append([voix,note])
        
        if time() >= self.oneTime*8 + self.debut_bar: #début de mesure par la fin de la precedente
           self.changeMesure()
        self.play_sound()

    def set_volume(self, volume_level):
        for voix in self.tab_voix:
            volume_message = mido.Message('control_change', channel=voix.channel, control=7, value=volume_level)
            voix.output_port.send(volume_message)

    def play_sound(self):
        for voix, note in self.to_play:
            note_on = mido.Message("note_on", note = note, channel = voix.channel, velocity = voix.velocity)
            voix.output_port.send(note_on)
        self.to_play = []  

    def stopSound(self):
        for voix in self.tab_voix:
            voix.stopSound()


    def change_all_tempos(self, tempo):
        for voix in self.tab_voix:
            voix.changeTempo(tempo)
            voix.bpm = tempo


    def changeMesure(self):
        print("Changement de mesure", end = " ")
        self.root, self.quality = boucle_accords.acc_suivi(self.tonic_init, self.quality_init, self.i_changement_acc)
        self.i_changement_acc = boucle_accords.nb_suiv(self.quality_init, self.i_changement_acc)
        self.debut_bar += self.oneTime*8
        print(self.root, self.quality, self.seventh)
        for voix in self.tab_voix:
            voix.changeParamMesure(self.root, self.quality)
            voix.changeMesure()

    def get_seventh(self):
        return self.seventh
    def get_root(self):
        return self.root
    def get_quality(self):
        return self.quality

    