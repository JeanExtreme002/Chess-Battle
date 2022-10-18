from .config import paths
from pyglet import media
import random

class SoundPlayer():
    """
    Classe para reproduzir sons.
    """
    
    def __init__(self, volume = 100, mute = False):
        self.__player = media.Player()
        self.set_volume(volume)
        self.set_mute(mute)

        self.__loaded_sounds = {
            "effects": {
                "starting": self.__load_sounds("effects", "starting"),
                "attacking": self.__load_sounds("effects", "attacking"),
                "dropping": self.__load_sounds("effects", "dropping"),
                "getting": self.__load_sounds("effects", "getting"),
                "invalid_movement": self.__load_sounds("effects", "invalid_movement"),
                "movement": self.__load_sounds("effects", "movement"),
                "victory": self.__load_sounds("effects", "victory")
            },
            "music": self.__load_sounds("music")
        }

        self.__played_musics = []

    def __load_sounds(self, *path):
        """
        Carrega todos os sons de um determinado diretório.
        """
        sounds = []

        for filename in paths.get_sound_list(*path):
            sounds.append(media.load(filename))
        return sounds

    def __play_sound(self, sound):
        """
        Reproduz um determinado som.
        """
        self.stop_sound()
        self.__player.queue(sound)
        self.__player.play()

    def is_muted(self):
        """
        Verifica se o reprodutor está ativado ou não.
        """
        return self.__muted

    def is_playing(self):
        """
        Verifica se algum som está sendo reproduzido.
        """
        return self.__player.playing

    def get_volume(self):
        """
        Retorna o volume do reprodutor.
        """
        return self.__volume

    def set_mute(self, boolean):
        """
        Ativa ou desativa o reprodutor.
        """
        self.__muted = boolean
        
        if boolean: self.__player.volume = 0
        else: self.__player.volume = self.__volume / 100
        
    def set_volume(self, value):
        """
        Define um volume para o reprodutor.
        """
        self.__volume = value
        self.__player.volume = self.__volume / 100
        
    def stop_sound(self):
        """
        Interrompe a reprodução de um som.
        """
        while self.is_playing():
            self.__player.next_source()

    def play_attacking_sound(self):
        """
        Reproduz som de ataque.
        """
        sound = random.choice(self.__loaded_sounds["effects"]["attacking"])
        self.__play_sound(sound)

    def play_dropping_sound(self):
        """
        Reproduz som de largar a peça selecionada.
        """
        sound = random.choice(self.__loaded_sounds["effects"]["dropping"])
        self.__play_sound(sound)

    def play_getting_sound(self):
        """
        Reproduz som de selecionar peça.
        """
        sound = random.choice(self.__loaded_sounds["effects"]["getting"])
        self.__play_sound(sound)

    def play_invalid_movement_sound(self):
        """
        Reproduz som de movimento inválido.
        """
        sound = random.choice(self.__loaded_sounds["effects"]["invalid_movement"])
        self.__play_sound(sound)
        
    def play_movement_sound(self):
        """
        Reproduz som de movimento.
        """
        sound = random.choice(self.__loaded_sounds["effects"]["movement"])
        self.__play_sound(sound)

    def play_music(self):
        """
        Reproduz uma música.
        """
        # Verifica se todas as músicas já foram reproduzidas. Se sim,
        # todas as músicas ficarão disponíveis novamente.
        if len(self.__loaded_sounds["music"]) == 0:
            self.__loaded_sounds["music"] = self.__played_musics
            self.__played_musics = []
            
        sound = random.choice(self.__loaded_sounds["music"])

        # Remove a música temporariamente da lista, para evitar
        # que a mesma seja reproduzida novamente.
        self.__played_musics.append(sound)
        self.__loaded_sounds["music"].remove(sound)
        
        self.__play_sound(sound)

    def play_start_sound(self):
        """
        Reproduz som de início de jogo.
        """
        sound = random.choice(self.__loaded_sounds["effects"]["starting"])
        self.__play_sound(sound)
    
    def play_victory_sound(self):
        """
        Reproduz som de vitória.
        """
        sound = random.choice(self.__loaded_sounds["effects"]["victory"])
        self.__play_sound(sound)
        
