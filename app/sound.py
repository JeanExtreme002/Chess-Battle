from .config import paths
import pyglet

####################################################################
class SoundPlayer():
    
    def __init__(self):
        self.__player = pyglet.media.Player()

    def __play_sound(self, filename):
        
        mediaLoad_music = pyglet.media.load(filename)
        self.__player.queue(mediaLoad_music)
        self.__player.play()
        
       
    
    def play_music(self):
        
        musicPath = paths.get_random_sound("music")
        self.__play_sound(musicPath)
        

    
    def stop_music(self):
        self.__player.next_source()
    
    
    def play_movement_sound(self):
        
       
        musicPath =r"C:\Users\ti-20\Downloads\sounds_effects_movement_moving_1.mp3"
        self.__play_sound(musicPath)
        
        
    
    def play_victory_sound(self):
        
      
        musicPath = r"C:\Users\ti-20\Downloads\sounds_effects_victory_victory_2.mp3"
        self.__play_sound(musicPath)
        








        
        
