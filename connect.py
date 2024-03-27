import interface2 as interface
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

    def launch(self):
        return self.algo.main()

    def quit(self):
        self.algo.quit = True
        self.algo.music_thread.join()
        self.algo.output_port.close()