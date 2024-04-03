import mido
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
import time
import gammes2 as gammes
import voix_structure_eucl as voix
import connect


class Algo:
    def __init__(self) -> None:
    
        #test variables
        self.vecteur_rythme_r = notes.norm(np.array([2, 4, 1, 3, 1, 0, 0, 0])) #le vecteur de proba des rythmes
        self.vecteur_rythme_l = np.array([0.2, 0.4, 0.15, 0.2, 0.05, 0, 0, 0]) #le vecteur de probabilité des rythmes

        self.vecteur_init = notes.gauss(notes.init_v(), 50)

        self.l_tab = [('A', 'Minor', ''), ('D', 'Minor', ''), ('G', 'Major', ''), ('C', 'Major', '')]
        self.scale = gammes.gamme('C', 'Major') 

        self.bpm = 120
        self.oneTime = 60/self.bpm

        self.nb_actif = 8 
        self.nb_tps = 32
        self.offset = 0
        # Variable to control music playback
        self.playing = False
        self.quit = False

        output_port_name = 'Microsoft GS Wavetable Synth 0'
        self.output_port = mido.open_output(output_port_name)

# Function to play music
    def play_music(self):
        print("Music playback started")
        listVoix = {}
        gauche = voix.VoixGauche(self.vecteur_init, self.vecteur_rythme_l, self.l_tab, self.scale, self.output_port, self.bpm)
        droite = voix.VoixDroite(self.vecteur_init, self.vecteur_rythme_r, self.l_tab, self.scale, self.output_port, self.bpm)
        #gauche_eucl = voix.VoixEuclideGauche(self.vecteur_init, self.vecteur_rythme_r, self.l_tab, self.scale, self.output_port, self.nb_actif, self.nb_tps, self.offset, self.bpm)
        listVoix["gauche"] = gauche
        listVoix["droite"] = droite
        #listVoix["gauche_eucl"] = gauche_eucl
        batch = 100
        k = 0
        while not self.quit :
            k+=1
            if self.playing :
                #on va laisser chaque voix décider de ce qu'ils veulent faire
                #si on a une nouvelle note à jouer, on l'ajoute dans notes
                #puis on joue toutes les notes d'un coup pour ne pas avoir de décalage.
                notes = {}
                t = time.time()
                for i in listVoix:
                    note = listVoix[i].nextTime(t)
                    if note:
                        notes[i] = note

                for i in notes:
                    note_on = mido.Message("note_on", note = notes[i], channel = listVoix[i].channel, velocity = listVoix[i].velocity)
                    listVoix[i].output_port.send(note_on)
                
                if (len(notes)>1):
                    print("simultaneous notes")
            else:
                time.sleep(0.1)
        
        print("Music playback stopped")


    # Set up MIDI output port (replace 'Your MIDI Port' with your actual MIDI output port name)
    def main(self):
        # Start the music playback in a separate thread
        self.music_thread = threading.Thread(target=self.play_music, args=())
        self.music_thread.start()
        
        return self.music_thread

    def close(self):
        self.music_thread.join()
        self.output_port.close()