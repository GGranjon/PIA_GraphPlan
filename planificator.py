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

        file = open(self.writing_path, "w")

        file.write(f"-----------------------------------------------------------------------------------------------------------------\n")
        file.write(f"----------------------------------------------- PROFONDEUR 0 ----------------------------------------------------\n")
        file.write(f"-----------------------------------------------------------------------------------------------------------------\n\n")

        file.write(f"------------------------ INITIAL PROPOSITIONS ------------------------\n\n")
        for prop in self.graph.layers[0]:
                file.write(f"{prop["name"]}\n")

        file.write(f"\n--------------------- INITIAL MUTEX PROPOSITIONS ---------------------\n\n")
        for prop in self.graph.mutex_per_layer[0]:
                file.write(f"{prop}\n")

        while not solved and n_iter < n_iter_lim:
            actions = find_actions(self.graph.layers[-1], self.objects)
            self.graph.add_layer(actions)

            mutex_actions = find_mutex_actions(actions, self.graph.mutex_per_layer[-1], self.graph.layers[-2])
            self.graph.add_mutex_layer(mutex_actions)

            propositions = find_propositions(self.graph.layers[-1])
            self.graph.add_layer(propositions)

            mutex_propositions = find_mutex_propositions(propositions, self.graph.mutex_per_layer[-1])
            self.graph.add_mutex_layer(mutex_propositions)

            file.write(f"\n-----------------------------------------------------------------------------------------------------------------\n")
            file.write(f"----------------------------------------------- PROFONDEUR {n_iter+1} ----------------------------------------------------\n")
            file.write(f"-----------------------------------------------------------------------------------------------------------------\n\n")

            file.write(f"------------------------------ ACTIONS -------------------------------\n\n")
            for i, action in enumerate(actions):
                file.write(f"{action["action"]}\n")

            file.write("\n-------------------------- NEW PROPOSITIONS --------------------------\n\n")
            for prop in propositions:
                file.write(f"{prop["name"]}\n")

            file.write("\n-------------------------- MUTEX ACTIONS -----------------------------\n\n")
            for mutex in mutex_actions:
                file.write(f"{actions[list(mutex)[0]]["action"], actions[list(mutex)[1]]["action"]}\n")
            
            file.write("\n------------------------ MUTEX PROPOSITIONS --------------------------\n\n")
            for mutex in mutex_propositions:
                file.write(f"{propositions[list(mutex)[0]]["name"], propositions[list(mutex)[1]]["name"]}\n")          

            if objectives_reachable(self.objectives, propositions, mutex_propositions):
                file.write("\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! OBJECTIVE IS THEORETICALLY REACHABLE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n")
                file.write("\n\n STARTING THE RESEARCH OF A SOLUTION \n\n")
                file.close()
                sol = find_solution(self.objectives, self.graph, len(self.graph.layers)-1, writing_path)
                file = open(writing_path, "a")
                if sol[0] == "success":
                    solved = True
            n_iter += 1
            print(n_iter)
        if solved:
            file.write("\n\nA SOLUTION HAS BEEN FOUND !\n\n")
        else:
            file.write("\n\nTHE SEARCH LIMIT HAS BEEN REACHED, NO SOLUTION FOUND\n\n")
        file.close()
        self.solution = sol
    
    def print_solution(self):
        if self.solution != None and self.solution[0] == "success":
            for action_layer in self.solution[1]:
                for action in list(action_layer):
                    if not "NOOP" in action:
                        print(f"{action}\n")
        else:
            print("Still no solution found")
    
    def write_solution(self, writing_path):
        file = open(writing_path, "a")
        if self.solution != None and self.solution[0] == "success":
            file.write(f"\nSOLUTION : \n\n")
            for action_layer in self.solution[1]:
                for action in list(action_layer):
                    if not "NOOP" in action:
                        file.write(f"{action}\n")
        else:
            None
        file.close()