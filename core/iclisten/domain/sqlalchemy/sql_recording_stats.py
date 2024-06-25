from sqlalchemy import Column, Integer, DateTime

from core.iclisten.domain.recording_stats import RecordingStats
from core.shared.domain.db import Base


class SQLRecordingStats(Base):
    __tablename__ = "recording_stats"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(DateTime, index=True)
    number_of_clicks = Column(Integer)
    recorded_minutes = Column(Integer)
    number_of_files = Column(Integer)

    def to_domain(self) -> RecordingStats:
        return RecordingStats(
            date_time=self.datetime,
            number_of_clicks=self.number_of_clicks,
            recorded_minutes=self.recorded_minutes,
            number_of_files=self.number_of_files
        )

    @staticmethod
    def from_domain(domain: RecordingStats) -> 'SQLRecordingStats':
        return SQLRecordingStats(
            datetime=domain.datetime,
            number_of_clicks=domain.number_of_clicks,
            recorded_minutes=domain.recorded_minutes,
            number_of_files=domain.number_of_files
        )
