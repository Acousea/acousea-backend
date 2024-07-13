from typing import List, Type

from sqlalchemy.orm import Session

from core.communication_system.domain.communicator.responses.drifter_summary_report_response import DrifterSummaryReportResponse
from core.iclisten.application.ports.iclisten_repository import PAMSystemRepository
from core.iclisten.domain.communicator.get_pam_device_info_response import GetPAMDeviceInfoCommunicationResponse
from core.iclisten.domain.communicator.pam_device_logging_config_response import PAMDeviceLoggingConfigCommunicationResponse
from core.iclisten.domain.communicator.pam_device_streaming_config_response import PAMDeviceStreamingConfigCommunicationResponse
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel
from core.iclisten.domain.pam_system_status_info_read_model import PAMDeviceStatusReadModel
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel
from core.iclisten.domain.recording_stats import RecordingStats
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel
from core.iclisten.domain.sqlalchemy.sql_pam_device_info import SQLPAMDeviceInfo
from core.iclisten.domain.sqlalchemy.sql_pam_device_logging_config import SQLPAMDeviceLoggingConfig
from core.iclisten.domain.sqlalchemy.sql_pam_device_streaming_config import SQLPAMDeviceStreamingConfig
from core.iclisten.domain.sqlalchemy.sql_recording_stats import SQLRecordingStats


class SQLitePAMSystemRepository(PAMSystemRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_pam_device_status_info(self) -> PAMDeviceStatusReadModel:
        # Query the database for the latest device status and convert it to the domain read model format
        device_status: Type[SQLPAMDeviceInfo] = (
            self.db.query(SQLPAMDeviceInfo)
            .order_by(SQLPAMDeviceInfo.timestamp.desc())
            .first()
        )

        if device_status is None:
            raise Exception("No recent device information found")

        return device_status.to_device_info_read_model()

    def add_pam_device_status_info(self, device_info: GetPAMDeviceInfoCommunicationResponse) -> None:
        # Convert the device info to the SQL model and store it in the database
        sql_device_info = SQLPAMDeviceInfo.from_get_device_info_response(device_info)
        self.db.add(sql_device_info)
        self.db.commit()

    def update_pam_device_status_info(self, drifter_summary_report_response: DrifterSummaryReportResponse) -> None:
        # Convert the device info to the SQL model and store it in the database
        sql_device_info = SQLPAMDeviceInfo.from_drifter_summary_report_response(drifter_summary_report_response)
        self.db.add(sql_device_info)
        self.db.commit()

    def get_logging_config(self) -> PAMDeviceLoggingConfigReadModel:
        # Query the database for the latest logging config and convert it to the domain read model format
        logging_config: Type[SQLPAMDeviceLoggingConfig] = (
            self.db.query(SQLPAMDeviceLoggingConfig)
            .order_by(SQLPAMDeviceLoggingConfig.timestamp.desc())
            .first()
        )

        if logging_config is None:
            raise Exception("No recent logging configuration found")

        return logging_config.to_device_config_read_model()

    def get_streaming_config(self) -> PAMDeviceStreamingConfigReadModel:
        # Query the database for the latest streaming config and convert it to the domain read model format
        streaming_config: Type[SQLPAMDeviceStreamingConfig] = (
            self.db.query(SQLPAMDeviceStreamingConfig)
            .order_by(SQLPAMDeviceStreamingConfig.timestamp.desc())
            .first()
        )

        if streaming_config is None:
            raise Exception("No recent streaming configuration found")

        return streaming_config.to_device_config_read_model()

    def add_pam_device_streaming_config(self,
                                        pam_device_streaming_config: PAMDeviceStreamingConfigCommunicationResponse):
        # Convert the streaming config to the SQL model and store it in the database
        sql_streaming_config = SQLPAMDeviceStreamingConfig.from_pam_device_streaming_config_response(pam_device_streaming_config)
        self.db.add(sql_streaming_config)
        self.db.commit()

    def get_latest_recording_stats(self, limit: int = 5) -> RecordingStatsReadModel:
        stats: List[Type[SQLRecordingStats]] = (
            self.db.query(SQLRecordingStats)
            .order_by(SQLRecordingStats.timestamp.desc())
            .limit(limit)
            .all()
        )
        domain_stats: List[RecordingStats] = [stat.to_domain() for stat in stats]
        datetime_clicks = [
            {"datetime": int(stat.epoch_time.timestamp()),
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

    def add_recording_stats_info(self, drifter_summary_report_response: DrifterSummaryReportResponse):
        # Convert the summary report response to the SQL model and store it in the database
        sql_stats = SQLRecordingStats.from_drifter_summary_report_response(drifter_summary_report_response)
        self.db.add(sql_stats)
        self.db.commit()

    def add_pam_device_logging_config(self, pam_device_logging_config: PAMDeviceLoggingConfigCommunicationResponse):
        # Convert the logging config to the SQL model and store it in the database
        sql_logging_config = SQLPAMDeviceLoggingConfig.from_pam_device_logging_config_response(pam_device_logging_config)
        self.db.add(sql_logging_config)
        self.db.commit()
