from planificator import Planificator
from actions_finder import find_actions
from propositions_finder import find_propositions
def main(path, writing_path):
    planificator = Planificator()
    planificator.DoPlan(path, writing_path)
    planificator.print_solution()

if __name__ == "__main__":
    path = "Exemples/r_fact3.txt"
    writing_path = "Traces/r_fact2.txt"
    main(path, writing_path)