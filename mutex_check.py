def are_propositions_mutex(p1, p2, graph, position):
    if position == 0:
        return False
    return are_prop_neg(p1, p2) or are_prop_support_mutex(p1, p2, graph, position)

def are_prop_neg(p1,p2):
    if (p1["type"] != p2["type"]):
        return False
    else:
        match p1["type"]:
            case "at":
                if p1["object"] != p2["object"] or p1["place"] == p2["place"]:
                    return False
                return True
            
            case "in":
                if p1["object"] != p2["object"] or p1["rocket"] == p2["rocket"]:
                    return False
                return True
            
            case "has_fuel":
                return p1["neg"] != p2["neg"]



def are_prop_support_mutex(p1, p2, graph, position):
    p1_actions = p1["actions"]
    p2_actions = p2["actions"]
    same_actions = list(set(p1_actions) & set(p2_actions))
    if len(same_actions) != 0:
        return False
    


def are_actions_mutex(a1, a2, graph, position):
    pass