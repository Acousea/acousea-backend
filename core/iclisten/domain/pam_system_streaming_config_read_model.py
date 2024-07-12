from pydantic import BaseModel


class PAMDeviceFFTStreamingConfig(BaseModel):
    record_fft: bool
    process_fft: bool
    fft_processing_type: int
    fft_interval: int
    fft_duration: int


class PAMDeviceWaveformStreamingConfig(BaseModel):
    record_waveform: bool
    process_waveform: bool
    waveform_processing_type: int
    waveform_interval: int
    waveform_duration: int


class PAMDeviceStreamingConfigReadModel(BaseModel):
    waveform_config: PAMDeviceWaveformStreamingConfig
    fft_config: PAMDeviceFFTStreamingConfig
    timestamp: str
