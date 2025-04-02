from parse_txt import parse_objects
from propositions import at_prop, in_prop, fuel_prop

def find_actions(proposition_layer, objects):
    return find_load_actions(proposition_layer, objects) + find_unload_actions(proposition_layer) + find_move_actions(proposition_layer, objects)

def find_load_actions(proposition_layer, objects):
    actions = []
    locations = {}
    for place in objects["PLACE"]:
        locations[place] = {"ROCKET": [], "CARGO": []}

    for prop in proposition_layer:  #Récupération des éléments à chaque lieu
        if prop["type"] == "at":
            obj_type = get_object_type(prop["object"], objects)
            location = prop["place"]
            locations[location][obj_type].append(prop["object"])
    
    for location in locations.keys():
        if (len(locations[location]["ROCKET"]) != 0) and (len(locations[location]["CARGO"]) != 0): #There are rockets and cargos
            for rocket in locations[location]["ROCKET"]:
                for cargo in locations[location]["CARGO"]:
                    actions.append({"action" : f"LOAD_{cargo}_{rocket}_{location}", "pre": [at_prop(cargo, location), at_prop(rocket, location)], "post": [in_prop(cargo, rocket), at_prop(cargo, location, neg = True)]})
    return actions

def find_unload_actions(proposition_layer):
    actions = []
    for prop in proposition_layer:
        if prop["type"] == "in":
            places = get_places(proposition_layer, prop["rocket"])
            for place in places:
                actions.append({"action" : f"UNLOAD_{prop["object"]}_{prop["rocket"]}_{place}", "pre" : [at_prop(prop["rocket"], place), in_prop(prop["object"], prop["rocket"])], "post" : [at_prop(prop["object"], place), in_prop(prop["object"], prop["rocket"], neg = True)]})
    return actions

def find_move_actions(proposition_layer, objects):
    actions = []
    rockets = {}
    for rocket in objects["ROCKET"]:
        rockets[rocket] = []
    for prop in proposition_layer:  #ajout des places visitées par chaque rocket
        if prop["type"] == "at" and prop["object"] in rockets.keys() and prop["place"] not in rockets[prop["object"]]:
            rockets[prop["object"]].append(prop["place"])
    for rocket in rockets.keys():
        for location_from in rockets[rocket]:
            for location_to in objects["PLACE"]:
                if location_from != location_to:
                    actions.append({"action" : f"MOVE_{rocket}_{location_from}_{location_to}", "pre" : [fuel_prop(rocket), at_prop(rocket, location_from)], "post" : [at_prop(rocket, location_to), fuel_prop(rocket, neg = True), at_prop(rocket, location_from, neg = True)]})
    return actions

def get_object_type(object_name, objects):
    for object_type in objects.keys():
        if object_name in objects[object_type]:
            return object_type
    raise Exception(f"Object {object_name} not found")

def get_places(proposition_layer, object_name):
    places = []
    for prop in proposition_layer:
        if prop["type"] == "at" and prop["object"] == object_name:
            places.append(prop["place"])
    return places