import interface as interface
import midoTest_objet_structure_eucl_interface as algo

class Connect:
    def __init__(self) -> None:
        self.algo = algo.Algo()
        self.thread = self.launch()

    def play_music(self, is_playing):
        if is_playing:
            self.algo.playing = True
        else:
            self.algo.playing = False
            self.algo.paused()
    def launch(self):
        return self.algo.main()
    
    def restart_music(self):
        self.algo.restart()
    
    def adjust_volume(self, volume_level):
        self.algo.set_channel_volume(int((volume_level / 100.0) * 127))

    def update_tempo(self, tempo):
        self.algo.bpm = tempo
        self.algo.oneTime = 60 / self.algo.bpm
        self.algo.orch.change_all_tempos(tempo)

    def set_instrument(self, voix, instrument):
        if instrument >= 0 and instrument < 128:
            self.algo.orch.jouees[voix] = True
            self.algo.orch.tab_voix[voix].choixInstrument(instrument)
        else :
            self.algo.orch.jouees[voix] = False
            print(self.algo.orch.jouees)

    def proba_fausse_note(self, proba):
        tab = self.algo.orch.tab_voix
        for i in range(len(tab)):
            tab[i].proba_faux = proba
    
    def quit(self):
        self.algo.quit = True
        self.algo.music_thread.join()
        self.algo.output_port.close()