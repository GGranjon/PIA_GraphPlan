from parse_txt import parse_txt_to_objects
from actions_finder import find_actions
from propositions_finder import find_propositions
from mutex_check import find_mutex_actions, find_mutex_propositions
from backward import objectives_reachable, find_solution
from graph import Graph
class Planificator():

    def __init__(self):
        self.objectives = []
        self.actions = ["MOVE", "LOAD", "UNLOAD"]
        self.objects = None
        self.graph = None
        self.solution = None

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
        n_iter_lim = 12
        solved = False
        sol = []
        while not solved and n_iter < n_iter_lim:
            actions = find_actions(self.graph.layers[-1], self.objects)
            self.graph.add_layer(actions)

            mutex_actions = find_mutex_actions(actions, self.graph.mutex_per_layer[-1], self.graph.layers[-2])
            self.graph.add_mutex_layer(mutex_actions)

            propositions = find_propositions(self.graph.layers[-1])
            self.graph.add_layer(propositions)

            mutex_propositions = find_mutex_propositions(propositions, self.graph.mutex_per_layer[-1])
            self.graph.add_mutex_layer(mutex_propositions)

            """print("----------------------- PROPOSITIONS --------------------")
            for prop in propositions:
                print(f"{prop}")
            print(f"---------------------- ACTIONS ----------------------")
            for i, action in enumerate(actions):
                print(f"{action["action"]} (index {i})\n")
            print("----------------------- MUTEX -------------------------")
            for mutex in mutex_actions:
                print(f"{actions[list(mutex)[0]]["action"], actions[list(mutex)[1]]["action"]}")"""
            if objectives_reachable(self.objectives, propositions, mutex_propositions):
                #print("!!!!!!!!!!!!!!!!!!!!!!!!!!! OBJECTIVE IS THEORETICALLY REACHABLE !!!!!!!!!!!!!!!!!!!!!!!!!")
                sol = find_solution(self.objectives, self.graph, len(self.graph.layers)-1)
                if sol[0] == "success":
                    solved = True
            n_iter += 1

        self.solution = sol
    
    def print_solution(self):
        if self.solution != None and self.solution[0] == "success":
            for action_layer in self.solution[1]:
                for action in list(action_layer):
                    if not "NOOP" in action:
                        print(f"{action}\n")
        else:
            print("Still no solution found")