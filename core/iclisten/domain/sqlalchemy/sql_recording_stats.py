import datetime

from sqlalchemy import Column, Integer, UUID, DateTime

from core.communication_system.domain.communicator.responses.drifter_summary_report_response import DrifterSummaryReportResponse
from core.iclisten.domain.recording_stats import RecordingStats
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLRecordingStats(Base):
    __tablename__ = "pam_recording_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    epoch_time = Column(DateTime, index=True)
    number_of_clicks = Column(Integer)
    recorded_minutes = Column(Integer)
    number_of_files = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    def to_domain(self) -> RecordingStats:
        return RecordingStats(
            epoch_time=self.timestamp,
            number_of_clicks=self.number_of_clicks,
            recorded_minutes=self.recorded_minutes,
            number_of_files=self.number_of_files
        )

    @staticmethod
    def from_domain(domain: RecordingStats) -> 'SQLRecordingStats':
        return SQLRecordingStats(
            id=GenericUUID.next_id(),
            epoch_time=domain.epoch_time,
            number_of_clicks=domain.number_of_clicks,
            recorded_minutes=domain.recorded_minutes,
            number_of_files=domain.number_of_files
        )

    @staticmethod
    def from_drifter_summary_report_response(drifter_summary_report_response: DrifterSummaryReportResponse) -> 'SQLRecordingStats':
        return SQLRecordingStats(
            id=GenericUUID.next_id(),
            epoch_time=datetime.datetime.utcfromtimestamp(drifter_summary_report_response.epoch_time),
            number_of_clicks=drifter_summary_report_response.audio_total_num_detections,
            recorded_minutes=drifter_summary_report_response.audio_recorded_minutes,
            number_of_files=drifter_summary_report_response.audio_num_files
        )


# Base.metadata.create_all(bind=engine) # This is done in the DBManager
