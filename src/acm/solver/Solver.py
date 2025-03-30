from acm.models.Input import Case, Machine
from pydantic import BaseModel, Field, model_validator
import heapq


class Solver(BaseModel):
    case: Case

    def __cashBeforeBuyingMachineOnDay(self, cash: int, m: Machine, day: int) -> int:
        if cash < m.P:
            return cash
        profitDays = day - m.D - 1
        possibleProfit = (cash - m.P) + profitDays * m.G + m.R

        return possibleProfit

    def solve(self) -> int:
        maxCash = self.case.C
        n = self.case.N

        # sorted list of machines
        machines = self.case.machines

        profits = [maxCash] * n

        for mIdx, machine in enumerate(machines):
            day = machine.D

            cashBeforeBuying = maxCash
            for mJdx in range(0, mIdx):
                if day == machines[mJdx].D:
                    continue
                profitOfMj = self.__cashBeforeBuyingMachineOnDay(
                    maxCash, machines[mJdx], day
                )
                if profitOfMj > cashBeforeBuying:
                    cashBeforeBuying = profitOfMj
            if cashBeforeBuying >= machine.P:
                profits[mIdx] = -(
                    (cashBeforeBuying - machine.P)
                    + machine.G * (self.case.D - day)
                    + machine.R
                )
            else:
                profits[mIdx] = -profits[mIdx]
        heapq.heapify(profits)
        return -profits[0]
