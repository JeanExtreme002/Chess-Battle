from .config import paths
import pyglet
import random

####################################################################
class SoundPlayer():
    
    def __init__(self):
        self.__player = pyglet.media.Player()

        self.__loaded_sounds = {
            "effects": {
                "starting": self.__load_sounds("effects", "starting"),
                "movement": self.__load_sounds("effects", "movement"),
                "victory": self.__load_sounds("effects", "victory")
            },
            "music": self.__load_sounds("music")
        }

    def __load_sounds(self, *path):
        sounds = []
        
        for filename in paths.get_sound_list(*path):
            sounds.append(pyglet.media.load(filename))
            
        return sounds

    def __play_sound(self, sound):
        self.stop_sound()
        self.__player.queue(sound)
        self.__player.play()
        
    def play_music(self):
        
        sound = random.choice(self.__loaded_sounds["music"])
        self.__play_sound(sound)
        
    def stop_sound(self):
        while self.is_playing():
            self.__player.next_source()
        
    def play_movement_sound(self):
       
        sound = random.choice(self.__loaded_sounds["effects"]["movement"])
        self.__play_sound(sound)

    def play_start_sound(self):
       
        sound = random.choice(self.__loaded_sounds["effects"]["starting"])
        self.__play_sound(sound)
    
    def play_victory_sound(self):
      
        sound = random.choice(self.__loaded_sounds["effects"]["victory"])
        self.__play_sound(sound)
        
    def is_playing(self):

        return self.__player.playing
