from copy import deepcopy

def find_propositions(action_layer):
    propositions = []
    for i, action in enumerate(action_layer):
        for prop in action["post"]:
            if not prop["neg"]:
                if already_added(propositions, prop):
                    index = get_index(propositions, prop)
                    propositions[index]["actions"].append(i)
                else:
                    propositions.append(deepcopy(prop))
                    propositions[-1]["actions"].append(i)
    return propositions

def already_added(propositions, prop):
    for prop2 in propositions:
        if prop2["type"] == prop["type"]:
            match prop["type"]:
                case "at":
                    if prop2["object"] == prop["object"] and prop2["place"] == prop["place"]:
                        return True
                case "in":
                    if prop2["object"] == prop["object"] and prop2["rocket"] == prop["rocket"]:
                        return True
                case "has_fuel":
                    if prop2["rocket"] == prop["rocket"]:
                        return True
    return False

def get_index(propositions, prop):
    for i, prop2 in enumerate(propositions):
        if prop2["type"] == prop["type"]:
            match prop["type"]:
                case "at":
                    if prop2["object"] == prop["object"] and prop2["place"] == prop["place"]:
                        return i
                case "in":
                    if prop2["object"] == prop["object"] and prop2["rocket"] == prop["rocket"]:
                        return i
                case "has_fuel":
                    if prop2["rocket"] == prop["rocket"]:
                        return i
    return -1

def get_indexes(propositions, list_prop):
    res = []
    for prop in list_prop:
        res.append(get_index(propositions, prop))
    return res
