from pydantic import BaseModel


class PAMDeviceFFTLoggingConfig(BaseModel):
    sample_rate: int
    fft_processing_type: int
    ffts_accumulated: int
    logging_mode: bool
    log_length: int


class PAMDeviceWaveformLoggingConfig(BaseModel):
    gain: int
    sample_rate: int
    bit_depth: int
    logging_mode: bool
    log_length: int


class PAMDeviceLoggingConfigReadModel(BaseModel):
    timestamp: str
    waveform_config: PAMDeviceWaveformLoggingConfig
    fft_config: PAMDeviceFFTLoggingConfig
