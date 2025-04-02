from parse_txt import parse_txt_to_objects

class Graph():
    def __init__(self):
        self.layers = []
        self.mutex_per_layer = []

    def add_layer(self, layer):
        self.layers.append(layer)
    
    def get_action_mutex(self):
        pass

    def get_proposition_mutex(self):
        pass
