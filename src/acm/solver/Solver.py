from acm.models.Input import Case, Machine
from typing import Optional, List
from pydantic import BaseModel, Field, model_validator
import heapq
from collections import deque


class Solver(BaseModel):
    case: Case
    dq: deque = None

    def __cashBeforeBuyingMachineOnDay(self, cash: int, m: Machine, day: int) -> int:
        if cash < m.P:
            return cash
        profitDays = day - m.D - 1
        possibleProfit = (cash - m.P) + profitDays * m.G + m.R

        return possibleProfit

    def solve_naive(self) -> int:
        maxCash = self.case.C
        n = self.case.N

        if n == 0:
            return maxCash
        # sorted list of machines
        machines: List[Machine] = self.case.machines

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

        profits.append(-maxCash)
        heapq.heapify(profits)
        return -profits[0]

    def evaluate(self, day: int, minVal: int) -> int:
        while len(self.dq) >= 2:
            m1, b1 = self.dq[0]
            m2, b2 = self.dq[1]
            if m1 * day + b1 >= m2 * day + b2:
                break
            self.dq.popleft()
        return self.dq[0][0] * day + self.dq[0][1] if self.dq else minVal

    def pushLine(self, pair: tuple[int, int], minVal: int):
        while len(self.dq) >= 2:
            m, b = pair
            m1, b1 = self.dq[-2]
            m2, b2 = self.dq[-1]

            x_prev = (b2 - b1) / (m1 - m2) if m1 != m2 else minVal
            x_new = (b - b2) / (m2 - m) if m != m2 else minVal
            if x_new <= x_prev:
                self.dq.pop()
            else:
                break
        self.dq.append(pair)

    def solve_opt(self) -> int:
        maxCash = self.case.C
        n = self.case.N
        self.dq = deque()

        # sorted list of machines
        machines = self.case.machines

        profits = [maxCash] * n

        for mIdx, machine in enumerate(machines):
            profit = profits[mIdx]
            current_cash = max(profit, self.evaluate(machine.D, self.case.C))
            profits[mIdx] = current_cash

            if current_cash >= machine.P:
                a, b = machine.getLine()
                b += current_cash
                self.pushLine((a, b), minVal=maxCash)
                profitDays = self.case.D - machine.D

                finalProfit = (
                    current_cash + machine.R - machine.P + machine.G * profitDays
                )
                if finalProfit > maxCash:
                    maxCash = finalProfit
        return maxCash
