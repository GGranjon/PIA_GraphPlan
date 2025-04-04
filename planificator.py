from parse_txt import parse_txt_to_objects
from actions_finder import find_actions
from propositions_finder import find_propositions
from mutex_check import find_mutex_actions, find_mutex_propositions
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
        self.graph.add_mutex_layer([])
    
    def DoPlan(self, r_facts):
        self.init_problem(r_facts)
        n_iter = 0
        n_iter_lim = 20
        solved = False
        while not solved and n_iter < n_iter_lim:
            actions = find_actions(self.graph.layers[-1], self.objects)
            self.graph.add_layer(actions)

            mutex_actions = find_mutex_actions(actions, self.graph.mutex_per_layer[-1], self.graph.layers[-2])
            self.graph.add_mutex_layer(mutex_actions)

            propositions = find_propositions(self.graph.layers[-1])
            self.graph.add_layer(propositions)

            mutex_propositions = find_mutex_propositions(propositions, self.graph.mutex_per_layer[-1])
            self.graph.add_mutex_layer(mutex_propositions)

            #if objectives_reachable(self.objectives, propositions):
            #    find_solution()

            n_iter += 1

        return self.graph.layers