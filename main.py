from planificator import Planificator

def main(path, writing_path):
    planificator = Planificator()
    planificator.DoPlan(path, writing_path)
    planificator.write_solution(writing_path)

if __name__ == "__main__":
    path = "Exemples/complexity9_example.txt"
    writing_path = "Traces/complexity9-trace.txt"
    main(path, writing_path)