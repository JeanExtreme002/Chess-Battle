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
        
       
        musicPath = paths.get_random_sound("effects","movement")
        self.__play_sound(musicPath)
        
        
    
    def play_victory_sound(self):
        
      
        musicPath = paths.get_random_sound("effects","victory")
        self.__play_sound(musicPath)
        



