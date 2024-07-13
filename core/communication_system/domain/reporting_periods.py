from pydantic import BaseModel


class ReportingPeriods(BaseModel):
    launchingSbdPeriod: int
    launchingLoraPeriod: int
    workingSbdPeriod: int
    workingLoraPeriod: int
    recoveringSbdPeriod: int
    recoveringLoraPeriod: int
