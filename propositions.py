def at_prop(obj : str, place : str, neg : bool = False, actions : list = []):
    return {"type" : "at", "neg" : neg, "object": obj, "place": place, "actions": actions}

def in_prop(obj : str, rocket : str, neg : bool = False, actions : list = []):
    return {"type": "in", "neg": neg, "object" : obj, "rocket": rocket, "actions": actions}

def fuel_prop(rocket : str, neg : bool = False, actions : list = []):
    return {"type": "has_fuel", "neg" : neg, "rocket" : rocket, "actions": actions}