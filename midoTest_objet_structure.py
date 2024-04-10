import mido
import pygame
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
from time import time
import gammes2 as gammes
import voix_structure as voix
import matplotlib.pyplot as plt

#test variables
vecteur_rythme_r = notes.norm(np.array([2, 4, 1, 3, 1, 0, 0, 0])) #le vecteur de proba des rythmes
vecteur_rythme_l = np.array([0.2, 0.4, 0.15, 0.2, 0.05, 0, 0, 0]) #le vecteur de probabilité des rythmes


vecteur_init = notes.gauss(notes.init_v(), 50)

l_tab = [('A', 'Minor', ''), ('D', 'Minor', ''), ('G', 'Major', ''), ('C', 'Major', '')]
scale = gammes.gamme('C', 'Major') 

bpm = 120
oneTime = 60/bpm


# Function to play music
def play_music():
    listVoix = {}
    gauche = voix.VoixGauche(vecteur_init, vecteur_rythme_l, l_tab, scale, output_port, bpm)
    droite = voix.VoixDroite(vecteur_init, vecteur_rythme_r, l_tab, scale, output_port, bpm)
    listVoix["gauche"] = gauche
    listVoix["droite"] = droite

    while not quit :
        if playing :
            #on va laisser chaque voix décider de ce qu'ils veulent faire
            #si on a une nouvelle note à jouer, on l'ajoute dans notes
            #puis on joue toutes les notes d'un coup pour ne pas avoir de décalage.
            notes = {}
            t = time()
            for i in listVoix:
                note = listVoix[i].nextTime(t)
                if note:
                    notes[i] = note

            for i in notes:
                note_on = mido.Message("note_on", note = notes[i], channel = listVoix[i].channel, velocity = listVoix[i].velocity)
                listVoix[i].output_port.send(note_on)            


# Initialize pygame for handling user input
pygame.init()

# Set up MIDI output port (replace 'Your MIDI Port' with your actual MIDI output port name)
output_port_name = 'Microsoft GS Wavetable Synth 0'
output_port = mido.open_output(output_port_name)


# Variable to control music playback
playing = True
quit = False

# Start the music playback in a separate thread
music_thread = threading.Thread(target=play_music, args=())
music_thread.start()

# Set up the Pygame window
width, height = 400, 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Music Generator')

# Font for text
font = pygame.font.Font(None, 36)

loop = -1
# Main loop for handling user input
while True:
    loop+=1
    for event in pygame.event.get():
        #print("got event")
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Toggle between playing and pausing the music
                playing = not playing
                if playing:
                    print("Resumed music.")
                else:
                    print("Paused music.")
            elif event.key == pygame.K_ESCAPE:
                # Exit the program
                playing = False
                quit = True
                pygame.quit()
                output_port.close()
                break
    
    # Update the display
    if quit:
        break
    screen.fill((255, 255, 255))

    # Display text
    text = font.render('Press SPACE to toggle playback', True, (0, 0, 0))
    screen.blit(text, (50, 50))

    pygame.display.flip()

    # Add a small delay to reduce CPU usage
    pygame.time.delay(10)
# Wait for the music thread to finish before exiting

music_thread.join()
pygame.quit()
