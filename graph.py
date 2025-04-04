from parse_txt import parse_txt_to_objects

class Graph():
    def __init__(self):
        self.layers = []
        self.mutex_per_layer = []

    def add_layer(self, layer):
        self.layers.append(layer)
    
    def add_mutex_layer(self, layer):
        self.mutex_per_layer.append(layer)