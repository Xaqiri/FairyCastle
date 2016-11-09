import random 

class BasicAI(): 
    def take_turn(self, player, map, objects): 
        monster = self.parent 
        if monster.visible: 
            if monster.distance_to(player) >= 1: 
                monster.move_towards(player.x, player.y, map, objects) 