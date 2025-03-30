from acm.models.Parser import Parser

from acm.solver.Solver import Solver


def main() -> None:
    url = "/Users/ayssar.mb/Desktop/dev/python/acm/src/data/example.txt"
    parser = Parser(filePath=url)
    res = parser.read()
    solver = Solver(case=res[0])

    print(solver.solve())
    print("-------------------------------------------------------")


main()

