from sqlalchemy.orm import Session

from core.shared.domain.db_dependencies import Base, engine, SessionLocal
from core.iclisten.domain.sqlalchemy.sql_recording_stats import SQLRecordingStats
from core.iclisten.domain.sqlalchemy.sql_pam_device_info import SQLPAMDeviceInfo
from core.communication_system.domain.sqlalchemy.sql_drifter_device_info import SQLDrifterDeviceInfo
from core.communication_system.domain.sqlalchemy.sql_localizer_device_info import SQLLocalizerDeviceInfo
from core.communication_system.domain.sqlalchemy.sql_rockblock_messages import SQLRockBlockMessage
from core.communication_system.domain.sqlalchemy.sql_communication_request_history import SQLCommunicationRequestHistory

print("Creating the database")
Base.metadata.create_all(bind=engine)


class DBManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def get_db(self) -> Session:
        db_session = self.SessionLocal()
        try:
            yield db_session
        finally:
            db_session.close()


if __name__ == "__main__":
    # Connect to the database and do a select on recording_stats
    """Warning. This script only works with the DATABASE_URL set to  sqlite:///../../../system.sqlite"""
    db = DBManager()
    with next(db.get_db()) as session:
        print("Connected to the database")
        print("Selecting from recording_stats")

        from core.iclisten.domain.sqlalchemy.sql_recording_stats import SQLRecordingStats

        stats = session.query(SQLRecordingStats).all()
        for stat in stats:
            print(stat.epoch_time, stat.number_of_clicks, stat.recorded_minutes, stat.number_of_files)
