class CombatComponent(): 
    def __init__(self, max_hp=100, max_mp=100, defense=10, strength=10, intelligence=10, xp=0, 
                    death_function=None, ai_component=None): 
        self.max_hp = max_hp 
        self.max_mp = max_mp 
        self.current_hp = max_hp 
        self.current_mp = max_mp 
        self.defense = defense 
        self.strength = strength 
        self.intelligence = intelligence 
        self.xp = xp 
        self.death_function = death_function 
        self.ai_component = ai_component 
        if self.ai_component: 
            self.ai_component.parent = self 

    def take_damage(self, damage, player): 
        self.current_hp -= damage 
        if self.current_hp <= 0: 
            self.current_hp = 0 
            function = self.death_function 
            if function is not None: 
                function(self.parent) 
            if self.parent is not player: 
                player.combat_component.xp += self.xp 

    def attack(self, target, player): 
        damage = self.strength - target.combat_component.defense 
        if damage > 0: 
            target.combat_component.take_damage(damage, player) 
        
    