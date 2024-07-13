import datetime

from sqlalchemy import Column, Integer, DateTime, UUID

from core.communication_system.domain.communicator.responses.drifter_reporting_periods_response import DrifterReportingPeriodsResponse
from core.communication_system.domain.reporting_periods import ReportingPeriods
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLDrifterReportingPeriods(Base):
    __tablename__ = "drifter_reporting_periods"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    launching_sbd_reporting_period_custom = Column(Integer, nullable=True)
    launching_lora_reporting_period_custom = Column(Integer, nullable=True)
    working_sbd_reporting_period_custom = Column(Integer, nullable=True)
    working_lora_reporting_period_custom = Column(Integer, nullable=True)
    recovering_sbd_reporting_period_custom = Column(Integer, nullable=True)
    recovering_lora_reporting_period_custom = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_reporting_periods(reporting_periods: ReportingPeriods) -> "SQLDrifterReportingPeriods":
        return SQLDrifterReportingPeriods(
            id=GenericUUID.next_id(),
            launching_sbd_reporting_period_custom=reporting_periods.launchingSbdPeriod,
            launching_lora_reporting_period_custom=reporting_periods.launchingLoraPeriod,
            working_sbd_reporting_period_custom=reporting_periods.workingSbdPeriod,
            working_lora_reporting_period_custom=reporting_periods.workingLoraPeriod,
            recovering_sbd_reporting_period_custom=reporting_periods.recoveringSbdPeriod,
            recovering_lora_reporting_period_custom=reporting_periods.recoveringLoraPeriod,
            timestamp=datetime.datetime.utcnow()
        )

    @staticmethod
    def from_drifter_reporting_periods_response(reporting_periods: DrifterReportingPeriodsResponse) -> "SQLDrifterReportingPeriods":
        return SQLDrifterReportingPeriods(
            id=GenericUUID.next_id(),
            launching_sbd_reporting_period_custom=reporting_periods.launching_sbd_period,
            launching_lora_reporting_period_custom=reporting_periods.launching_lora_period,
            working_sbd_reporting_period_custom=reporting_periods.working_sbd_period,
            working_lora_reporting_period_custom=reporting_periods.working_lora_period,
            recovering_sbd_reporting_period_custom=reporting_periods.recovering_sbd_period,
            recovering_lora_reporting_period_custom=reporting_periods.recovering_lora_period,
            timestamp=datetime.datetime.utcnow()
        )

    def to_reporting_periods(self) -> ReportingPeriods:
        return ReportingPeriods(
            launchingSbdPeriod=self.launching_sbd_reporting_period_custom,
            launchingLoraPeriod=self.launching_lora_reporting_period_custom,
            workingSbdPeriod=self.working_sbd_reporting_period_custom,
            workingLoraPeriod=self.working_lora_reporting_period_custom,
            recoveringSbdPeriod=self.recovering_sbd_reporting_period_custom,
            recoveringLoraPeriod=self.recovering_lora_reporting_period_custom
        )
