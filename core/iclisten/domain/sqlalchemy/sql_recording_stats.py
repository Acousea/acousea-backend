from sqlalchemy import UUID, Column, Integer, DateTime

from core.iclisten.domain.recording_stats import RecordingStats
from core.shared.domain.db_dependencies import Base, engine
from core.shared.domain.value_objects import GenericUUID


class SQLRecordingStats(Base):
    __tablename__ = "recording_stats"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
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
            id=GenericUUID.next_id(),
            datetime=domain.datetime,
            number_of_clicks=domain.number_of_clicks,
            recorded_minutes=domain.recorded_minutes,
            number_of_files=domain.number_of_files
        )


# Base.metadata.create_all(bind=engine) # This is done in the DBManager
