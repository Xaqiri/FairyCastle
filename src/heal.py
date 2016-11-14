class Heal(): 
    def __init__(self, amount=10): 
        self.amount = amount 
        
    def use(self, entity=None): 
        if entity.combat_component.current_hp < entity.combat_component.max_hp: 
            entity.combat_component.current_hp += self.amount 
            if entity.combat_component.current_hp > entity.combat_component.max_hp: 
                entity.combat_component.current_hp = entity.combat_component.max_hp 
            return 'used' 
        return 'cancelled'