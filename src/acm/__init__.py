import os
from pathlib import Path

import click

from acm.models.Parser import Parser
from acm.solver.Solver import Solver


@click.command()
@click.argument("file", type=str)
def main(file):
    expandedPath = os.path.expanduser(file)
    inputPath = Path(expandedPath)

    if not inputPath.exists():
        click.echo(f"Error: File not found at {inputPath}", err=True)
        return

    parser = Parser(filePath=inputPath)
    cases = parser.read()
    # cases = [cases[2]]
    for caseId, case in enumerate(cases):
        opt = Solver(case=case).solve_opt()
        print(f"Case {caseId + 1}: {opt}")


# main()
