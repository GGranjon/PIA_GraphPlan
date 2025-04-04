from planificator import Planificator
from actions_finder import find_actions
from propositions_finder import find_propositions
def main(path):
    planificator = Planificator()
    planificator.DoPlan(path)
    for i, layer in enumerate(planificator.graph.layers):
        print(f"---------------------- LAYER {i} ------------------------------\n\n")
        print(f"---------------------- ELEMENTS ------------------------------\n\n")
        for elt in layer:
            print(elt, "\n")
        print(f"---------------------- MUTEX ------------------------------\n\n")
        print(planificator.graph.mutex_per_layer[i])

if __name__ == "__main__":
    path = "Exemples/r_fact_perso2.txt"
    main(path)