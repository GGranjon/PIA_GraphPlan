from propositions_finder import get_index
from graph import Graph
from itertools import product
from joblib import Parallel, delayed

def objectives_reachable(objectives, propositions, mutex_propositions):
    objectives_indexes = []
    for prop in objectives:
        index = get_index(propositions, prop)
        if index == -1:
            return False
        objectives_indexes.append(index)
    for i in range(len(objectives_indexes)-1):
        for j in range(i+1, len(objectives_indexes)):
            couple = {i,j}
            if couple in mutex_propositions:
                return False
    return True

def process_action_combo(combo, actions, graph, layer_index):
    """
    Traitement d'une combinaison d'actions pour en déduire les nouveaux objectifs.
    C'est la fonction qui sera parallélisée.
    """
    new_objectives = []
    for action_index in combo:
        action_preconditions = actions[action_index]["pre"]
        for precond in action_preconditions:
            if precond not in new_objectives:
                new_objectives.append(precond)
    
    # Appel de la fonction find_solution pour chaque combinaison d'actions
    sol_combo = find_solution(new_objectives, graph, layer_index - 2)
    return sol_combo

def find_solution(objectives, graph: Graph, layer_index):
    #print(f"--------------------------- LAYER {layer_index} ------------------------------")
    if layer_index == 0:    # Base case scenario
        if objectives_reachable(objectives, graph.layers[0], []):
            return ["success", []]

    propositions = graph.layers[layer_index]
    mutex_propositions = graph.mutex_per_layer[layer_index]
    actions = graph.layers[layer_index-1]
    mutex_actions = graph.mutex_per_layer[layer_index-1]

    indexes = []
    for objective in objectives :
        index = get_index(propositions, objective)
        if index == -1 :
            raise Exception("prop not found")
        indexes.append(index)
    objectives = [propositions[index] for index in indexes]

    actions_per_objective = {}
    for i, objective in enumerate(objectives):
        actions_per_objective[i] = objective["actions"]
        #print(objective)
        #print(f"OBJECTIF {i} : {[actions[index]["action"] for index in objective["actions"]]}")
    
    action_combinations = find_valid_action_combinations(actions_per_objective, mutex_actions)
    if len(action_combinations) == 0:
            #print("------------------- NO COMBINATION OF ACTIONS FOUND -----------------")
            return ["fail", []]
    else:
        for combo in action_combinations:
            new_objectives = []
            for action_index in combo:
                action_preconditions = actions[action_index]["pre"]
                for precond in action_preconditions:
                    if precond not in new_objectives:
                        new_objectives.append(precond)

            sol_combo = find_solution(new_objectives, graph, layer_index-2)
            if sol_combo[0] == "success":
                new_sol = sol_combo[1]
                actions_this_step = set({})
                for index in combo:
                    actions_this_step.add(actions[index]["action"])
                new_sol.append(actions_this_step)
                return ["success", new_sol]
        return ["fail", []]

def find_valid_action_combinations(actions_for_props, mutex_actions):
    """
    Find all valid combinations of actions that achieve all propositions without mutex conflicts.
    
    :param actions_for_props: Dictionary {proposition: list of possible action indexes}
    :param mutex_pairs: List of sets of mutex action pairs
    :return: List of valid action sets
    """
    # Generate all possible combinations: each proposition picks one action
    all_combinations = list(product(*actions_for_props.values()))
    valid_combinations = []
    
    for combination in all_combinations:
        if not contains_mutex_pair(combination, mutex_actions) and set(combination) not in valid_combinations:
            valid_combinations.append(set(combination))  # Store as set for easy comparison
    valid_combinations = sorted(valid_combinations, key=len)
    return reduce_action_combinations(valid_combinations)


def contains_mutex_pair(combination, mutex_pairs):
    """
    Check if a combination of actions contains any mutex pair.
    
    :param combination: A tuple representing a selection of actions
    :param mutex_pairs: List of sets of mutex action pairs
    :return: True if there's a mutex conflict, False otherwise
    """
    combination_set = set(combination)
    for mutex in mutex_pairs:
        if mutex.issubset(combination_set):  # Check if all elements of mutex are in combination
            return True  # Conflict found
    return False


def reduce_action_combinations(valid_combinations):
    """
    Reduce the list of valid action combinations by removing redundant ones.
    The original list is sorted by length of its elements
    A combination is redundant if it is a superset of another combination.
    
    :param valid_combinations: List of sets of action combinations
    :return: Reduced list of action combinations
    """
    reduced_list = []
    for elt in valid_combinations:
        not_superset = True
        i = 0
        while not_superset and i < len(reduced_list):
            if elt.issuperset(reduced_list[i]):
                not_superset = False
            i += 1
        if not_superset:
            reduced_list.append(elt)
    return reduced_list