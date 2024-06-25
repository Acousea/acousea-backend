import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///system.sqlite"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()
metadata = MetaData()


class DBManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal

    def get_db(self) -> Session:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()


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
            print(stat.datetime, stat.number_of_clicks, stat.recorded_minutes, stat.number_of_files)
