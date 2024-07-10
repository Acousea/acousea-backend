from pydantic import BaseModel


class PAMDeviceFFTStreamingConfigReadModel(BaseModel):
    record_fft: bool
    process_fft: bool
    fft_processing_type: str
    fft_interval: int
    fft_duration: int


class PAMDeviceWaveformStreamingConfigReadModel(BaseModel):
    record_waveform: bool
    process_waveform: bool
    waveform_processing_type: str
    waveform_interval: int
    waveform_duration: int


class PAMDeviceStreamingConfigReadModel(BaseModel):
    waveform_config: PAMDeviceWaveformStreamingConfigReadModel
    fft_config: PAMDeviceFFTStreamingConfigReadModel
    timestamp: str
