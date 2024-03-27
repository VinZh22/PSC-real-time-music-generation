import mido
import pygame
import threading
import main_gauche2 as main_gauche
import main_droite2 as main_droite
import notes2 as notes
import numpy as np
from time import time
import gammes2 as gammes
import random as rd
import boucle_accords

#J'ai modifié dans if boolnote_r dans new_note, avec la proba que la note soit fausse. Il faut créer le paramètre proba_faux au bon endroit par contre (reste très faible globalement, mais devient plus élevée quand la musique doit être angoissante,...
#J'ai modifié la façon de changer d'accord (j'ai rajouté tonic_init, quality_init, gamme_init et i_changement_acc; par contre j'ai enlevé l_tab et i_tab.

#test variables
vecteur_rythme_r = notes.norm(np.array([2, 4, 1, 3, 1, 0, 0, 0])) #le vecteur de proba des rythmes
vecteur_rythme_l = np.array([0.2, 0.4, 0.15, 0.2, 0.05, 0, 0, 0]) #le vecteur de probabilité des rythmes


vecteur_init = notes.gauss(notes.init_v(), 50)

tonic_init = rd.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
quality_init = rd.choice(['Major', 'Minor'])
gamme_init = (tonic_init, quality_init)

#l_tab = [('A', 'Minor', ''), ('D', 'Minor', ''), ('G', 'Major', ''), ('C', 'Major', '')]
#gamme_init = l_tab[3][:2]
scale = gammes.gamme(gamme_init) 

bpm = 120
oneTime = 60/bpm


# Function to play music
def play_music(output_port):

    i_changement_acc = 1
    #i_tab = 0 #position dans la progression d'accord
    boolnote_r = True #indique le besoin de générer une nouvelle note
    boolnote_l = True
    #len_tab = len(l_tab)
    v_r = notes.f_gamme(vecteur_init, scale)
    v_l = notes.f_gamme(vecteur_init, scale)
    vrtm = vecteur_rythme_r
    
    debut_bar = time() - 8*oneTime
    rtm_l = main_gauche.nouvelle_structure_rythmique(vecteur_rythme_l)
    i_rtm_l = 0
    len_rtm_l = len(rtm_l)
        
    #root, quality, seventh = l_tab[0]
    seventh = "Dominant"
    root, quality = gamme_init
    liste_first_tab = gammes.accord(root, quality, seventh)
    
    v_l = notes.f_gamme(v_l, gammes.accord(root, quality, seventh))
    liste_notes_l = []
    
    for i in range(0, len_rtm_l):
        new_note_l = main_droite.gen(v_l)
        liste_notes_l.append(new_note_l)

    #la liste des positions des notes dans l'accord
    l_indices_l = notes.search_indices(liste_first_tab, liste_notes_l) 
    
    while playing:
            
        #on gère le changement d'accord
        if time() >= oneTime*8 + debut_bar: #début de mesure par la fin de la precedente
            #root, quality, seventh = l_tab[i_tab]
            #i_tab = (i_tab + 1)%len_tab
            root, quality = boucle_accords.acc_suivi(tonic_init, quality_init, i_changement_acc)
            i_changement_acc = boucle_accords.nb_suiv(quality_init, i_changement_acc)
            debut_bar += oneTime*8
            
            #main droite
            v_r = notes.f_newtab(v_r, root, quality, seventh)
            
            #main gauche : juste besoin des notes de l'accord
            l_notes_l = gammes.accord(root, quality, seventh)

        #on gère l'arrivée d'une nouvelle note
        if boolnote_r:
            tp = main_droite.gen(vrtm) + 1 #le nombre de temps de la note que l'on va jouer
            t_end = time() + tp*oneTime
            new_note = main_droite.gen(v_r) + rd.choices([-1,0,1], weights=[proba_faux/2, 1-proba_faux, proba_faux/2], k=1)[0] # utilise la proba proba_faux à paramétrer selon l'ambiance
            note_on = mido.Message('note_on', note = new_note, velocity = 64) #on enclenche la note
            output_port.send(note_on) #et on commence à la jouer
            boolnote_r = False #indique qu'une note est jouée
            v_r = notes.f_note(v_r, new_note) #la fonction qui modifie v à chaque note
        
        #on regarde si on peut jouer une nouvelle note
        if time() > t_end:
            note_off = mido.Message('note_off', note = new_note)
            output_port.send(note_off)
            boolnote_r = True
            
        if boolnote_l:
            tp_l = rtm_l[i_rtm_l]  #le nombre de temps de la note que l'on va jouer
            i_rtm_l = (i_rtm_l + 1)%len_rtm_l
            t_end_l = time() + tp_l*oneTime
            new_note_l = l_notes_l[l_indices_l[i_rtm_l]]
            note_on_l = mido.Message('note_on', note = new_note_l, velocity = 64) #on enclenche la note
            output_port.send(note_on_l) #et on commence à la jouer
            boolnote_l = False #indique qu'une note est jouée
        
        #on regarde si on peut jouer une nouvelle note
        if time() > t_end_l:
            note_off_l = mido.Message('note_off', note = new_note_l)
            output_port.send(note_off_l)
            boolnote_l = True
                

# Initialize pygame for handling user input
pygame.init()

# Set up MIDI output port (replace 'Your MIDI Port' with your actual MIDI output port name)
output_port_name = 'Microsoft GS Wavetable Synth 0'
output_port = mido.open_output(output_port_name)

# Variable to control music playback
playing = True

# Start the music playback in a separate thread
music_thread = threading.Thread(target=play_music, args=(output_port,))
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
                pygame.quit()
                break
    
    # Update the display
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
