import datetime
from sqlalchemy import Column, Integer, DateTime, UUID, Boolean, SmallInteger, String

from core.iclisten.domain.communicator.get_pam_device_logging_config_response import GetPAMDeviceLoggingConfigCommunicationResponse
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel, PAMDeviceWaveformLoggingConfigReadModel, \
    PAMDeviceFFTLoggingConfigReadModel
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLPAMDeviceLoggingConfig(Base):
    __tablename__ = "pam_device_logging_config"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    log_waveform = Column(Boolean)
    gain = Column(SmallInteger)
    waveform_sample_rate = Column(Integer)
    waveform_logging_mode = Column(SmallInteger)
    waveform_log_length = Column(SmallInteger)
    bit_depth = Column(SmallInteger)
    endianness = Column(String)
    log_fft = Column(Boolean)
    reference_level = Column(SmallInteger)
    fft_sample_rate = Column(Integer)
    points_per_fft = Column(SmallInteger)
    fft_processing_type = Column(SmallInteger)
    samples_between_ffts = Column(SmallInteger)
    ffts_accumulated = Column(SmallInteger)
    fft_weighting_factor = Column(SmallInteger)
    fft_logging_mode = Column(SmallInteger)
    fft_log_length = Column(SmallInteger)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_get_device_config_response(response: GetPAMDeviceLoggingConfigCommunicationResponse) -> "SQLPAMDeviceLoggingConfig":
        bit_depth, endianness = SQLPAMDeviceLoggingConfig.get_bit_depth_and_endianness(response.data_format)
        return SQLPAMDeviceLoggingConfig(
            id=GenericUUID.next_id(),
            log_waveform=bool(response.log_waveform),
            gain=response.gain,
            waveform_sample_rate=response.waveform_sample_rate,
            waveform_logging_mode=response.waveform_logging_mode,
            waveform_log_length=response.waveform_log_length,
            bit_depth=bit_depth,
            endianness=endianness,
            log_fft=bool(response.log_fft),
            reference_level=response.reference_level,
            fft_sample_rate=response.fft_sample_rate,
            points_per_fft=response.points_per_fft,
            fft_processing_type=response.fft_processing_type,
            samples_between_ffts=response.samples_between_ffts,
            ffts_accumulated=response.ffts_accumulated,
            fft_weighting_factor=response.fft_weighting_factor,
            fft_logging_mode=response.fft_logging_mode,
            fft_log_length=response.fft_log_length,
            timestamp=response.timestamp
        )

    def to_device_config_read_model(self) -> PAMDeviceLoggingConfigReadModel:
        return PAMDeviceLoggingConfigReadModel(
            timestamp=self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            waveform_config=PAMDeviceWaveformLoggingConfigReadModel(
                log_waveform=self.log_waveform,
                gain=self.gain,
                sample_rate=self.waveform_sample_rate,
                logging_mode=self.get_logging_mode_description(self.waveform_logging_mode),
                log_length=self.waveform_log_length,
                bit_depth=self.bit_depth,
                endianness=self.endianness
            ),
            fft_config=PAMDeviceFFTLoggingConfigReadModel(
                log_fft=self.log_fft,
                reference_level=self.reference_level,
                sample_rate=self.fft_sample_rate,
                points_per_fft=self.points_per_fft,
                fft_processing_type=self.get_fft_processing_type_description(self.fft_processing_type),
                samples_between_ffts=self.samples_between_ffts,
                ffts_accumulated=self.ffts_accumulated,
                fft_weighting_factor=self.fft_weighting_factor,
                logging_mode=self.get_logging_mode_description(self.fft_logging_mode),
                log_length=self.fft_log_length
            )
        )

    @staticmethod
    def get_logging_mode_description(mode: int) -> str:
        mode_map = {
            0: "Disabled",
            1: "Active",
            2: "Active when triggered"
        }
        return mode_map.get(mode, "Unknown")

    @staticmethod
    def get_bit_depth_and_endianness(format_code: int) -> (int, str):
        format_map = {
            2: (16, "Big Endian"),
            3: (24, "Big Endian"),
            4: (32, "Big Endian"),
            130: (16, "Little Endian"),
            131: (24, "Little Endian"),
            132: (32, "Little Endian")
        }
        return format_map.get(format_code, (0, "Unknown"))

    @staticmethod
    def get_fft_processing_type_description(type_code: int) -> str:
        type_map = {
            4: "Mean Average",
            5: "Peak Detect",
            6: "Exponential Moving Average"
        }
        return type_map.get(type_code, "Unknown")

# Base.metadata.create_all(bind=engine) # Esto se hace en el DBManager
