from propositions import at_prop, in_prop, fuel_prop

def parse_txt_to_objects(path):
    """
    Parses a text file containing information about places, rockets, cargos, 
    and objectives, and converts it into structured Python objects.
    Args:
        path (str): The file path to the text file to be parsed.
    Returns:
        tuple: A tuple containing:
            - places (list): A list of place names.
            - rockets (dict): A dictionary with informations about the rockets.
            - cargos (dict): A dictionary with informations about the cargos.
            - objectives (dict): A dictionary with the different objectives that shall be reached.
    """

    objects = {"ROCKET":[], "CARGO":[], "PLACE":[]}
    propositions = []
    objectives = []


    file = open(path, "r")
    lines = file.readlines()
    file.close()

    in_preconds = False
    in_effects = False

    for line in lines:
        line = line.strip()
        if line == "":
            continue

        if line.startswith("(preconds"):
            in_preconds = True
            in_effects = False
            continue

        if line.startswith("(effects"):
            in_effects = True
            in_preconds = False
            continue

        if in_preconds:
            # Parse preconditions
            tokens = line.strip("()").split()
            if tokens[0] == "at":
                obj_name, place_name = tokens[1], tokens[2]
                propositions.append(at_prop(obj_name, place_name))

            elif tokens[0] == "has-fuel":
                rocket_name = tokens[1]
                propositions.append(fuel_prop(rocket_name))
                
            elif tokens[0] == "in":
                obj_name, rocket_name = tokens[1], tokens[2]
                propositions.append(in_prop(obj_name,rocket_name))

        elif in_effects:
            # Parse objectives (effects)
            tokens = line.strip("()").split()
            if tokens[0] == "at":
                obj_name, place_name = tokens[1], tokens[2]
                objectives.append(at_prop(obj_name, place_name))

        else:
            # Parse objects (Place, Rocket, Cargo)
            tokens = line.strip("()").split()
            name, obj_type = tokens[0], tokens[1]
            objects[obj_type].append(name)

    return objects, propositions, objectives

def parse_objects(path):
    objects = {"ROCKET":[], "CARGO":[], "PLACE":[]}
    file = open(path, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("(preconds"):
            return objects
        else:
            # Parse objects (Place, Rocket, Cargo)
            tokens = line.strip("()").split()
            name, obj_type = tokens[0], tokens[1]
            objects[obj_type].append(name)