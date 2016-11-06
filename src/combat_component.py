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
        if death_function: 
            self.death_function.parent = self 
        self.ai_component = ai_component 
        if self.ai_component: 
            self.ai_component.parent = self 
