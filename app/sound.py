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
        self.stop_sound()
        self.__play_sound(musicPath)
        
    def stop_sound(self):
        self.__player.pause()
        self.__player.delete()
        
        
    def play_movement_sound(self):
       
        musicPath = paths.get_random_sound("effects", "movement")
        self.stop_sound()
        self.__play_sound(musicPath)
    
    def play_victory_sound(self):
      
        musicPath = paths.get_random_sound("effects", "victory")
        self.stop_sound()
        self.__play_sound(musicPath)
        
    def is_playing(self):

        return self.__player.playing
