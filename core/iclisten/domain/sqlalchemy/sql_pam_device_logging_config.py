import datetime

from sqlalchemy import Column, Integer, DateTime, UUID, SmallInteger

from core.iclisten.domain.communicator.pam_device_logging_config_response import PAMDeviceLoggingConfigCommunicationResponse
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel, PAMDeviceWaveformLoggingConfig, \
    PAMDeviceFFTLoggingConfig
from core.shared.domain.db_dependencies import Base
from core.shared.domain.value_objects import GenericUUID


class SQLPAMDeviceLoggingConfig(Base):
    __tablename__ = "pam_device_logging_config"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)

    # Waveform (WAV)
    gain = Column(SmallInteger)
    waveform_sample_rate = Column(Integer)
    waveform_logging_mode = Column(SmallInteger)
    waveform_log_length = Column(SmallInteger)
    bit_depth = Column(SmallInteger)

    # Spectrum (FFT)
    fft_sample_rate = Column(Integer)
    fft_processing_type = Column(SmallInteger)  #
    ffts_accumulated = Column(SmallInteger)
    fft_logging_mode = Column(SmallInteger)
    fft_log_length = Column(SmallInteger)

    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def from_pam_device_logging_config_response(response: PAMDeviceLoggingConfigCommunicationResponse) -> "SQLPAMDeviceLoggingConfig":
        return SQLPAMDeviceLoggingConfig(
            id=GenericUUID.next_id(),

            gain=response.gain,
            waveform_sample_rate=response.waveform_sample_rate,
            waveform_logging_mode=response.waveform_logging_mode,
            waveform_log_length=response.waveform_log_length,
            bit_depth=response.bit_depth,

            fft_sample_rate=response.fft_sample_rate,
            fft_processing_type=response.fft_processing_type,
            ffts_accumulated=response.ffts_accumulated,
            fft_logging_mode=response.fft_logging_mode,
            fft_log_length=response.fft_log_length,

            timestamp=datetime.datetime.utcnow()
        )

    def to_device_config_read_model(self) -> PAMDeviceLoggingConfigReadModel:
        return PAMDeviceLoggingConfigReadModel(
            timestamp=self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            waveform_config=PAMDeviceWaveformLoggingConfig(
                gain=self.gain,
                sample_rate=self.waveform_sample_rate,
                logging_mode=self.waveform_logging_mode,
                log_length=self.waveform_log_length,
                bit_depth=self.bit_depth,
            ),
            fft_config=PAMDeviceFFTLoggingConfig(
                sample_rate=self.fft_sample_rate,
                fft_processing_type=self.fft_processing_type,
                ffts_accumulated=self.ffts_accumulated,
                logging_mode=self.fft_logging_mode,
                log_length=self.fft_log_length
            )
        )

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
