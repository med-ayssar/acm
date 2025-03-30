from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from typing_extensions import Self


class Machine(BaseModel):
    D: int = Field(ge=1)
    P: int = Field(ge=1)
    R: int = Field(ge=1)
    G: int = Field(ge=1)
    Id: int
    Case: int

    @model_validator(mode="after")
    def postCheck(self) -> Self:
        if self.R >= self.P:
            raise ValueError(
                f"The resale price R = {self.R} of the Machine {self.id} of TestCase {
                    self.Case
                } is larger than its purchase price"
            )
        return self

    @staticmethod
    def getFields() -> List[str]:
        return list(Machine.model_fields.keys())


class Case(BaseModel):
    N: int = Field(le=12**9)
    C: int = Field(ge=1, le=10**9)
    D: int = Field(ge=1, le=10**9)
    Id: int
    machines: Optional[List[Machine]] = []

    @model_validator(mode="after")
    def postCheck(self) -> Self:
        for machine in self.machines:
            if machine.D > self.D:
                raise ValueError(
                    f"The availabity day of the Machine {
                        machine.Id
                    } is larger than the number of Days in the TestCase {self.Id}"
                )
        self.__sortMachines()
        return self

    @staticmethod
    def getFields() -> List[str]:
        return list(Case.model_fields.keys())

    def __sortMachines(self) -> None:
        self.machines.sort(key=lambda m: m.D)
