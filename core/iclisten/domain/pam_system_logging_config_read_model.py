from pydantic import BaseModel


class PAMDeviceFFTLoggingConfigReadModel(BaseModel):
    log_fft: bool
    reference_level: int
    sample_rate: int
    points_per_fft: int
    fft_processing_type: str
    samples_between_ffts: int
    ffts_accumulated: int
    fft_weighting_factor: int
    logging_mode: str
    log_length: int


class PAMDeviceWaveformLoggingConfigReadModel(BaseModel):
    log_waveform: bool
    gain: int
    sample_rate: int
    logging_mode: str
    log_length: int
    bit_depth: int
    endianness: str


class PAMDeviceLoggingConfigReadModel(BaseModel):
    timestamp: str
    waveform_config: PAMDeviceWaveformLoggingConfigReadModel
    fft_config: PAMDeviceFFTLoggingConfigReadModel
