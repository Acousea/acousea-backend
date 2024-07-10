import datetime

from sqlalchemy import Column, Integer, DateTime, UUID, Boolean

from core.iclisten.domain.communicator.get_pam_device_streaming_config_response import GetPAMDeviceStreamingConfigCommunicationResponse
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel, PAMDeviceWaveformStreamingConfigReadModel, \
    PAMDeviceFFTStreamingConfigReadModel
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLPAMDeviceStreamingConfig(Base):
    __tablename__ = "pam_device_streaming_config"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    record_waveform = Column(Boolean)
    process_waveform = Column(Boolean)
    waveform_processing_type = Column(Integer)
    waveform_interval = Column(Integer)
    waveform_duration = Column(Integer)
    record_fft = Column(Boolean)
    process_fft = Column(Boolean)
    fft_processing_type = Column(Integer)
    fft_interval = Column(Integer)
    fft_duration = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_get_device_config_response(response: GetPAMDeviceStreamingConfigCommunicationResponse) -> "SQLPAMDeviceStreamingConfig":
        return SQLPAMDeviceStreamingConfig(
            id=GenericUUID.next_id(),
            record_waveform=bool(response.record_waveform),
            process_waveform=bool(response.process_waveform),
            waveform_processing_type=response.waveform_processing_type,
            waveform_interval=response.waveform_interval,
            waveform_duration=response.waveform_duration,
            record_fft=bool(response.record_fft),
            process_fft=bool(response.process_fft),
            fft_processing_type=response.fft_processing_type,
            fft_interval=response.fft_interval,
            fft_duration=response.fft_duration,
            timestamp=response.timestamp
        )

    def to_device_config_read_model(self) -> PAMDeviceStreamingConfigReadModel:
        return PAMDeviceStreamingConfigReadModel(
            waveform_config=PAMDeviceWaveformStreamingConfigReadModel(
                record_waveform=self.record_waveform,
                process_waveform=self.process_waveform,
                waveform_processing_type=self.get_waveform_processing_type_description(self.waveform_processing_type),
                waveform_interval=self.waveform_interval,
                waveform_duration=self.waveform_duration
            ),
            fft_config=PAMDeviceFFTStreamingConfigReadModel(
                record_fft=self.record_fft,
                process_fft=self.process_fft,
                fft_processing_type=self.get_fft_processing_type_description(self.fft_processing_type),
                fft_interval=self.fft_interval,
                fft_duration=self.fft_duration
            ),
            timestamp=self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        )

    @staticmethod
    def get_waveform_processing_type_description(type: int) -> str:
        type_map = {
            0: "None",
            1: "Teager-Kaiser Energy Operator",
        }
        return type_map.get(type, "Unknown")

    @staticmethod
    def get_fft_processing_type_description(type: int) -> str:
        type_map = {
            0: "None",
            1: "Magnitude Calculation",
        }
        return type_map.get(type, "Unknown")

# Base.metadata.create_all(bind=engine) # This is done in the DBManager
