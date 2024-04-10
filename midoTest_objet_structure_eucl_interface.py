import mido
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
import time
import gammes2 as gammes
import voix_eucl_2 as voix
import connect
import random as rd

def detect_synthesizers():
    # Get list of MIDI input and output devices
    input_devices = mido.get_input_names()
    output_devices = mido.get_output_names()
    
    # Initialize lists to store synthesizers
    synthesizers = []

    # Check if a device name contains "synth", "keyboard", "virtual" or other keywords indicating it's a synthesizer
    synth_keywords = ["synth", "keyboard", "virtual", "soft", "midi through"]
    
    # Iterate through input devices
    for device in input_devices:
        for keyword in synth_keywords:
            if keyword in device.lower():
                synthesizers.append({'name': device, 'type': 'input'})
                break  # Once found, no need to check further keywords

    # Iterate through output devices
    for device in output_devices:
        for keyword in synth_keywords:
            if keyword in device.lower():
                synthesizers.append({'name': device, 'type': 'output'})
                break  # Once found, no need to check further keywords

    return synthesizers

class Algo:
    def __init__(self) -> None:
    
        #test variables
        self.vecteur_rythme_r = notes.norm(np.array([2, 4, 1, 3, 1, 0, 0, 0])) #le vecteur de proba des rythmes
        self.vecteur_rythme_l = np.array([0.2, 0.4, 0.15, 0.2, 0.05, 0, 0, 0]) #le vecteur de probabilité des rythmes

        self.vecteur_init = notes.gauss(notes.init_v(), 50)

        self.l_tab = [('A', 'Minor', ''), ('D', 'Minor', ''), ('G', 'Major', ''), ('C', 'Major', '')]
        self.scale = gammes.gamme('C', 'Major') 

        self.tonic_init = rd.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        self.quality_init = rd.choice(['Major', 'Minor'])
        self.gamme_init = (self.tonic_init, self.quality_init)

        self.bpm = 120
        self.oneTime = 60/self.bpm

        self.nb_actif = 8 
        self.nb_tps = 32
        self.offset = 0
        # Variable to control music playback
        self.playing = False
        self.quit = False

        synths = detect_synthesizers()
        output_port_name = synths[0]['name']
        self.output_port = mido.open_output(output_port_name)


# Function to play music
    def play_music(self):
        print("Music playback started")
        listVoix = {}
        gauche = voix.VoixGauche(self.vecteur_init, self.vecteur_rythme_l, self.scale, self.output_port, self.bpm)
        droite = voix.VoixDroite(self.vecteur_init, self.vecteur_rythme_r, self.scale, self.output_port, self.bpm)
        gauche_eucl = voix.VoixEuclideGauche(self.vecteur_init, self.vecteur_rythme_r, self.scale, self.output_port, self.nb_actif, self.nb_tps, self.offset, self.bpm)
        listVoix = [gauche]
        self.orch = voix.Orchestre(self.tonic_init, self.quality_init, self.gamme_init, listVoix)
        while not self.quit :
            if self.playing :
                #on va laisser chaque voix décider de ce qu'ils veulent faire
                #si on a une nouvelle note à jouer, on l'ajoute dans notes
                #puis on joue toutes les notes d'un coup pour ne pas avoir de décalage.
                self.orch.nextTime(time.time())
                time.sleep(self.oneTime/2)
            else:
                time.sleep(0.1)
        
        print("Music playback stopped")

    def paused(self):
        self.orch.stopSound()

    # Set up MIDI output port (replace 'Your MIDI Port' with your actual MIDI output port name)
    def main(self):
        # Start the music playback in a separate thread
        self.music_thread = threading.Thread(target=self.play_music, args=())
        self.music_thread.start()
        
        return self.music_thread

    def close(self):
        self.music_thread.join()
        self.output_port.close()