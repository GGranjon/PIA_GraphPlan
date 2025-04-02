from planificator import Planificator
from actions_finder import find_actions
def main(path):
    planificator = Planificator()
    planificator.DoPlan(path)
    prop_layer = planificator.graph.layers[0]
    objects = planificator.objects
    print("\n\n",find_actions(prop_layer, objects))

if __name__ == "__main__":
    path = "Exemples/r_fact_perso.txt"
    main(path)