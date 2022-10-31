from asyncore import write
import os
import shutil  

class GameData():
    
    game_id = len(os.listdir(dir))
    def __init__(self):
        temp = open(self.dir+"/temp.txt","w")
        temp.write("vamos")
    def add_game(self):
        game_id += 1
    def step(self,jogadas):
        temp = open(self.dir+"/temp.txt","a")
        temp.write(jogadas+"\n")
    def won_game(self,winner):
        game_name="/"
        if(winner == 0):
            game_name += "W"
        if(winner == 1):
            game_name += "B"
        tbww=str(self.game_id)
        while(len(tbww)<4):
            tbww= "0" + tbww
            
        game_name +=tbww
        gn = open(self.dir+game_name,"w")
        shutil.copyfile(self.dir+"/temp.txt",self.dir+game_name)
        
#print(type(GameData.dir))
obj = GameData()
print(GameData.game_id)
#obj.won_game(0)
obj.step("k1,l2,p3")
obj.step("k1,l2,p3")
