from typing import List, Type

from sqlalchemy.orm import Session

from core.iclisten.application.ports.iclisten_repository import ICListenRepository
from core.iclisten.domain.communicator.get_device_info_response import GetDeviceInfoResponse
from core.iclisten.domain.iclisten_device_info_read_model import ICListenDeviceInfoReadModel
from core.iclisten.domain.job_setup_read_model import JobSetupReadModel
from core.iclisten.domain.recording_stats import RecordingStats
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.iclisten.domain.sqlalchemy.sql_iclisten_device_info import SQLICListenDeviceInfo
from core.iclisten.domain.sqlalchemy.sql_recording_stats import SQLRecordingStats


class SQLiteICListenRepository(ICListenRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_device_info(self) -> ICListenDeviceInfoReadModel:
        # Query the database for the latest device status and convert it to the domain read model format
        device_status: Type[SQLICListenDeviceInfo] = (
            self.db.query(SQLICListenDeviceInfo)
            .order_by(SQLICListenDeviceInfo.timestamp.desc())
            .first()
        )

        if device_status is None:
            raise Exception("No recent device information found")

        return device_status.to_device_info_read_model()

    def add_device_info(self, device_info: GetDeviceInfoResponse) -> None:
        # Convert the device info to the SQL model and store it in the database
        sql_device_info = SQLICListenDeviceInfo.from_get_device_info_response(device_info)
        self.db.add(sql_device_info)
        self.db.commit()

    def get_job_setup(self) -> JobSetupReadModel:
        # response_packet = self.communicator.send_request(GetJobSetupRequest())
        # job_status: GetJobResponse = GetJobResponse(response_packet)
        pass

    def get_latest_stats(self, limit: int = 5) -> RecordingStatsReadModel:
        stats: List[Type[SQLRecordingStats]] = (
            self.db.query(SQLRecordingStats)
            .order_by(SQLRecordingStats.datetime.desc())
            .limit(limit)
            .all()
        )
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
