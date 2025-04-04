from propositions_finder import get_index

def find_mutex_propositions(propositions, mutex_actions, is_first_layer = False):
    """returns a list of couples of propositions that are mutex. Using the index position of the propositions"""
    if is_first_layer:
        return []
    list_mutex = []
    for i, prop1 in enumerate(propositions):
        for j, prop2 in enumerate(propositions):
            if i<j:
                if are_prop_neg(prop1, prop2) or are_prop_support_mutex(prop1, prop2, mutex_actions):
                    list_mutex.append({i,j})
    return list_mutex

def are_prop_neg(p1,p2):
    if (p1["type"] != p2["type"]):
        return False
    else:
        match p1["type"]:
            case "at":
                return p1["object"] == p2["object"] and p1["place"] != p2["place"]
            
            case "in":
                return p1["object"] == p2["object"] and p1["rocket"] != p2["rocket"]
            
            case "has_fuel":
                return p1["neg"] != p2["neg"]

def are_prop_support_mutex(p1, p2, actions_mutex):
    p1_actions = p1["actions"]
    p2_actions = p2["actions"]
    same_actions = list(set(p1_actions) & set(p2_actions))
    if len(same_actions) != 0:
        return False
    for action1 in p1_actions:
        for action2 in p2_actions:
            if {action1, action2} not in actions_mutex:
                return False
    return True

def find_mutex_actions(actions, mutex_propositions, propositions):
    list_mutex = []
    for i, action1 in enumerate(actions):
        for j, action2 in enumerate(actions):
            if i < j:
                if are_actions_inconsistent(action1, action2) or are_actions_interference(action1, action2) or are_actions_conflict(action1, action2, mutex_propositions, propositions):
                    list_mutex.append({i,j})
    return list_mutex

def are_actions_inconsistent(a1, a2):
    """checks if some effects cancel each other"""
    post_a1 = a1["post"]
    post_a2 = a2["post"]
    for prop1 in post_a1:
        for prop2 in post_a2:
            if are_prop_neg(prop1, prop2):
                return True
    return False

def are_actions_interference(a1,a2):
    """checks if one cancels a precondition of the other"""
    post_a1 = a1["post"]
    post_a2 = a2["post"]
    pre_a1 = a1["pre"]
    pre_a2 = a2["pre"]
    for prop1 in post_a1:
        for prop2 in pre_a2:
            if are_prop_neg(prop1, prop2):
                return True
    for prop1 in post_a2:
        for prop2 in pre_a1:
            if are_prop_neg(prop1, prop2):
                return True
    return False

def are_actions_conflict(a1,a2, mutex_propositions, propositions):
    """checks if the preconditions are mutex"""
    pre_a1 = a1["pre"]
    pre_a2 = a2["pre"]
    for prop1 in pre_a1:
        for prop2 in pre_a2:
            index1 = get_index(propositions, prop1)
            index2 = get_index(propositions, prop2)
            if {index1, index2} in mutex_propositions:
                return True
    return False
