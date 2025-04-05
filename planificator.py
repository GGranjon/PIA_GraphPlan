from parse_txt import parse_txt_to_objects
from actions_finder import find_actions
from propositions_finder import find_propositions
from mutex_check import find_mutex_actions, find_mutex_propositions
from backward import objectives_reachable, find_solution
from graph import Graph
class Planificator():

    def __init__(self):
        self.objectives = []
        self.objects = None
        self.graph = None
        self.solution = None

    def init_problem(self,path, writing_path=None):
        objects, propositions, objectives = parse_txt_to_objects(path)
        self.objectives = objectives
        self.objects = objects
        self.graph = Graph()
        self.graph.add_layer(propositions)
        self.graph.add_mutex_layer([])
        self.writing_path = writing_path
    
    def DoPlan(self, r_facts, writing_path):
        self.init_problem(r_facts, writing_path)
        n_iter = 0
        n_iter_lim = 7
        solved = False
        sol = []

        #file = open(self.writing_path, "w")

        while not solved and n_iter < n_iter_lim:
            actions = find_actions(self.graph.layers[-1], self.objects)
            self.graph.add_layer(actions)

            mutex_actions = find_mutex_actions(actions, self.graph.mutex_per_layer[-1], self.graph.layers[-2])
            self.graph.add_mutex_layer(mutex_actions)

            propositions = find_propositions(self.graph.layers[-1])
            self.graph.add_layer(propositions)

            mutex_propositions = find_mutex_propositions(propositions, self.graph.mutex_per_layer[-1])
            self.graph.add_mutex_layer(mutex_propositions)
            """file.write(f"------------------------ PROFONDEUR {n_iter} ------------------------\n")
            file.write("----------------------- PROPOSITIONS --------------------\n")
            for prop in propositions:
                file.write(f"{prop}\n")
            file.write(f"---------------------- ACTIONS ----------------------")
            for i, action in enumerate(actions):
                file.write(f"{action["action"]} (index {i})\n")
            file.write("----------------------- MUTEX -------------------------")
            for mutex in mutex_actions:
                file.write(f"{actions[list(mutex)[0]]["action"], actions[list(mutex)[1]]["action"]}")"""

            if objectives_reachable(self.objectives, propositions, mutex_propositions):
                #print("!!!!!!!!!!!!!!!!!!!!!!!!!!! OBJECTIVE IS THEORETICALLY REACHABLE !!!!!!!!!!!!!!!!!!!!!!!!!\n")
                sol = find_solution(self.objectives, self.graph, len(self.graph.layers)-1, writing_path)
                if sol[0] == "success":
                    solved = True
            n_iter += 1
            print(n_iter)
        #file.close()

        self.solution = sol
    
    def print_solution(self):
        if self.solution != None and self.solution[0] == "success":
            for action_layer in self.solution[1]:
                for action in list(action_layer):
                    if not "NOOP" in action:
                        print(f"{action}\n")
        else:
            print("Still no solution found")