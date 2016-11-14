class Item(): 
    def __init__(self, use_component=None): 
        self.use_component = use_component 
        if self.use_component: 
            self.use_component.parent = self 

    def pick_up(self, inventory, objects=None, function=None): 
        inventory.append(self.parent) 
        #objects.remove(self.parent) 
        print('You picked up a {}!'.format(self.parent.name)) 
    
    def drop(self, inventory, objects, player): 
        objects.append(self.parent) 
        inventory.remove(self.parent) 
        self.parent.x = player.x 
        self.parent.y = player.y 
        print('You dropped a {}.'.format(self.parent.name)) 
    
    def use(self, entity): 
        function = self.use_component.use(entity) 
        if function is None: 
            print("The {} can't be used.".format(self.parent.name)) 
        elif function is 'cancelled': 
            print("You're already at full health.") 
        else: 
            if function is not 'cancelled': 
                entity.inventory.remove(self.parent) 