from pydantic import BaseModel, model_validator, Field
from pathlib import Path
import re

from typing import List
from acm.models.Input import Case, Machine
from enum import Enum


class Parser(BaseModel):
    filePath: Path = Field(..., description="A valid file path")

    @model_validator(mode="after")
    def checkFileExists(cls, values):
        filePath = values.filePath
        if not filePath.exists():
            raise ValueError(f"File does not exist: {filePath}")
        if not filePath.is_file():
            raise ValueError(f"Path is not a file: {filePath}")
        return values

    def parse(self) -> List[tuple[List[str], List[List[str]]]]:
        with open(self.filePath, "r") as inputDesc:
            lines = inputDesc.readlines()

            case_pattern = r"^[0-9]+\s[0-9]+\s[0-9]+$"
            machine_pattern = r"^[0-9]+\s[0-9]+\s[0-9]+\s[0-9]+$"
            end_pattern = r"^0\s0\s0$"

            groups = []
            currentCase = None
            caseMachines = []

            readLines = 0
            for line in lines:
                line = line.strip()
                line = re.sub(r"\s+", " ", line)

                if re.match(case_pattern, line):
                    if currentCase is not None:
                        groups.append((currentCase, caseMachines))
                    caseMachines = []
                    currentCase = line.split()
                elif re.match(machine_pattern, line):
                    caseMachines.append(line.split())
                elif re.match(end_pattern, line):
                    if currentCase is not None:
                        groups.append((currentCase, caseMachines))
                    caseMachines = []
                    currentCase = line.split()
                    break
                else:
                    raise ValueError(f"Parser: Unexpected sequence {line}")
                readLines += 1
            if readLines != len(lines):
                raise ValueError(
                    f"Parser: Early '000' sequnce at line {readLines} terminated the scan"
                )
            return groups

    def read(self) -> List[Case]:
        res = self.parse()
        cases = []
        caseField = Case.getFields()
        machineFields = Machine.getFields()
        for idx, item in enumerate(res):
            case = item[0]
            machines = item[1]
            m = []
            for mIdx, machine in enumerate(machines):
                machine.extend([mIdx, idx])
                data = dict(zip(machineFields, machine))
                m.append(Machine(**data))
            case.extend([idx, m])
            data = dict(zip(caseField, case))
            cases.append(Case(**data))
        return cases
