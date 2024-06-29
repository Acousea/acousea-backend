from sqlalchemy.orm import Session
from typing import List, Type

from core.iclisten.domain.recording_stats import RecordingStats
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.iclisten.domain.sqlalchemy.sql_recording_stats import SQLRecordingStats


class RecordingStatsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_latest_stats(self, limit: int = 5) -> RecordingStatsReadModel:

        print("Getting latest stats")
        stats: List[Type[SQLRecordingStats]] = (
            self.db.query(SQLRecordingStats)
            .order_by(SQLRecordingStats.datetime.desc())
            .limit(limit)
            .all()
        )
        print("Query executed")
        domain_stats: List[RecordingStats] = [stat.to_domain() for stat in stats]
        datetime_clicks = [
            {"datetime": int(stat.datetime.timestamp()),
             "num_clicks": int(stat.number_of_clicks)} for stat in domain_stats
        ]
        total_num_clicks = sum(stat.number_of_clicks for stat in domain_stats)
        total_recorded_minutes = sum(stat.recorded_minutes for stat in domain_stats)
        total_number_of_files = sum(stat.number_of_files for stat in domain_stats)

        return RecordingStatsReadModel(
            datetime_clicks=datetime_clicks,
            total_num_clicks=int(total_num_clicks),
            total_recorded_minutes=int(total_recorded_minutes),
            total_number_of_files=int(total_number_of_files)
        )

