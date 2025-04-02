from planificator import Planificator
from actions_finder import find_actions
from propositions_finder import find_propositions
def main(path):
    planificator = Planificator()
    print(planificator.DoPlan(path))
    for i, layer in enumerate(planificator.graph.layers):
        print(f"---------------------- LAYER {i} ------------------------------\n\n")
        for elt in layer:
            print(elt, "\n")

if __name__ == "__main__":
    path = "Exemples/r_fact_perso2.txt"
    main(path)