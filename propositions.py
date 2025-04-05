def at_prop(obj : str, place : str, neg : bool = False, actions : list = []):
    if not neg:
        return {"type" : "at", "neg" : neg, "object": obj, "place": place, "actions": actions, "name": f"at_{obj}_{place}"}
    else:
        return {"type" : "at", "neg" : neg, "object": obj, "place": place, "actions": actions, "name": f"at_{obj}_{place}_neg"}

def in_prop(obj : str, rocket : str, neg : bool = False, actions : list = []):
    if not neg:
        return {"type": "in", "neg": neg, "object" : obj, "rocket": rocket, "actions": actions, "name": f"in_{obj}_{rocket}"}
    else:
        return {"type": "in", "neg": neg, "object" : obj, "rocket": rocket, "actions": actions, "name": f"in_{obj}_{rocket}_neg"}

def fuel_prop(rocket : str, neg : bool = False, actions : list = []):
    if not neg:
        return {"type": "has_fuel", "neg" : neg, "rocket" : rocket, "actions": actions, "name": f"has_fuel_{rocket}"}
    else:
        return {"type": "has_fuel", "neg" : neg, "rocket" : rocket, "actions": actions, "name": f"has_fuel_{rocket}_neg"}