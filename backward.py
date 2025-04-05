from propositions_finder import get_index
from graph import Graph
from itertools import product
from joblib import Parallel, delayed

def objectives_reachable(objectives, propositions, mutex_propositions):
    if len(objectives) == 1:
        return get_index(propositions, objectives[0]) != -1
    if len(objectives) == 0:
        return True
    objectives_indexes = []
    for prop in objectives:
        index = get_index(propositions, prop)
        if index == -1:
            return False
        objectives_indexes.append(index)
    for i in range(len(objectives_indexes)-1):
        for j in range(i+1, len(objectives_indexes)):
            couple = {objectives_indexes[i],objectives_indexes[j]}
            if couple in mutex_propositions:
                return False
    return True

def process_action_combo(combo, actions, graph, layer_index, file_path):
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
    sol_combo = find_solution(new_objectives, graph, layer_index - 2, file_path)
    return sol_combo

def find_solution(objectives, graph: Graph, layer_index, file_path):
    file = open(file_path, "a")
    file.write(f"\n--------------------------- LAYER {layer_index} ------------------------------\n")

    parallel = True
    if layer_index == 0:    # Base case scenario
        if objectives_reachable(objectives, graph.layers[layer_index], []):
            file.write("\nOBJECTIVES ARE NOT MUTEX AT LAYER 0\n")
            return ["success", []]
        else:
            file.write("\nOBJECTIVES ARE MUTEX AT LAYER 0\n")
            return ["fail", []]
    
    propositions = graph.layers[layer_index]
    mutex_propositions = graph.mutex_per_layer[layer_index]
    actions = graph.layers[layer_index-1]
    mutex_actions = graph.mutex_per_layer[layer_index-1]
    
    indexes = []
    for objective in objectives :
        index = get_index(propositions, objective)
        if index == -1 :
            raise Exception("proposition not found")
        indexes.append(index)
    objectives = [propositions[index] for index in indexes]

    file.write("\n-------------------- OBJECTIVES -------------------------\n")
    for obj in objectives:
        file.write(f"{obj["name"]}\n")

    if not objectives_reachable(objectives, graph.layers[layer_index], mutex_propositions):
        file.write("\nOBJECTIVES ARE MUTEX\n")
        return ["fail", []]
    file.write("\nOBJECTIVES ARE NOT MUTEX\n")

    actions_per_objective = {}
    for i, objective in enumerate(objectives):
        actions_per_objective[i] = objective["actions"]
    
    action_combinations = find_valid_action_combinations(actions_per_objective, mutex_actions)
    if len(action_combinations) == 0:
            file.write("\n------------------- NO COMBINATION OF ACTIONS FOUND -----------------\n")
            return ["fail", []]
    else:
        if parallel:
            file.write("\n STARTING PARALLEL RESEARCH OF A SOLUTION IN THE SET OF ACTIONS THAT GIVES OUR OBJECTIVES\n")
            file.close()
            solutions = Parallel(n_jobs=-1)(delayed(process_action_combo)(combo, actions, graph, layer_index, file_path) for combo in action_combinations)
            file = open(file_path, "a")
            for k, sol_combo in enumerate(solutions):
                if sol_combo[0] == "success":
                    file.write("\n A SET OF ACTIONS MAKING OUR OBJECTIVES HAS BEEN FOUND DOABLE IN THE PREVIOUS LAYER\n")
                    new_sol = sol_combo[1]
                    actions_this_step = set({})
                    for index in action_combinations[k]:
                        actions_this_step.add(actions[index]["action"])
                    new_sol.append(actions_this_step)
                    return ["success", new_sol]
            file.write("\n NO SET OF ACTIONS THAT GIVE OUR OBJECTIVES ARE DOABLE\n")
        else:
            for combo in action_combinations:
                new_objectives = []
                for action_index in combo:
                    action_preconditions = actions[action_index]["pre"]
                    for precond in action_preconditions:
                        if precond not in new_objectives:
                            new_objectives.append(precond)
                sol_combo = find_solution(new_objectives, graph, layer_index - 2, file_path)
                if sol_combo[0] == "success":
                    new_sol = sol_combo[1]
                    actions_this_step = set({})
                    for index in combo:
                        actions_this_step.add(actions[index]["action"])
                    new_sol.append(actions_this_step)
                    return ["success", new_sol]
        file.close()
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
    return valid_combinations #reduce_action_combinations(valid_combinations)


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