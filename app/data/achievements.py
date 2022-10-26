import json, time

__all__ = ("UserAchievements",)

class UserAchievements(object):
    """
    Classe para carregar e salvar
    as conquistas do jogador.
    """

    def __init__(self, filename, crypter):
        self.__filename = filename
        self.__crypter = crypter

        self.__achievements = {}
        self.__load_achievements()

    def __load_achievements(self):
        """
        Carrega as conquistas do arquivo.
        """
        try:
            file = open(self.__filename, encoding = "UTF-8")
            
            data = self.__crypter.decrypt(file.read())
            self.__achievements.update(json.loads(data))
            
            file.close()
            
        finally: return self.__save_achievements()

    def __save_achievements(self):
        """
        Salva as conquistas em um arquivo.
        """
        with open(self.__filename, "w", encoding = "UTF-8") as file:
            string = json.dumps(self.__achievements)
            file.write(self.__crypter.encrypt(string))

    def add_achievement(self, title, description = ""):
        """
        Adiciona uma nova conquista.
        """
        if title in self.__achievements: return False
        
        self.__achievements[title] = {
            "description": description,
            "time": time.time()
        }
        self.__save_achievements()
        return True

    def get_achievements(self):
        """
        Retorna a lista de todas as conquistas ordenada por data e hora.
        """
        achievements = []
        
        for key, value in self.__achievements.items():
            achievements.append([key, value["description"], value["time"]])
        achievements.sort(key = lambda value: value[-1])

        for title, description, reg_time in achievements:
            reg_time = time.strftime("%d/%m/%y às %H:%M",time.localtime(reg_time))
            yield title, description, reg_time

