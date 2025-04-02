from parse_txt import parse_txt_to_objects
from graph import Graph
class Planificator():

    def __init__(self):
        self.objectives = []
        self.actions = ["MOVE", "LOAD", "UNLOAD"]
        self.objects = None
        self.graph = None

    def init_problem(self,path):
        objects, propositions, objectives = parse_txt_to_objects(path)
        self.objectives = objectives
        self.objects = objects
        self.graph = Graph()
        self.graph.add_layer(propositions)
    
    def DoPlan(self, r_facts):
        self.init_problem(r_facts)