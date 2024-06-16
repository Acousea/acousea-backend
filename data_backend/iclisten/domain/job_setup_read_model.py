from typing import Literal, Optional

from pydantic import BaseModel, conint, Field


class WaveFormSetupReadModel(BaseModel):
    gain: Literal[0, 6, 12, 18, 24, 30, 36, 42, 48]  # Gain in dB
    sample_rate: Literal[
        1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000
    ]  # Sample Rate in samples per second
    logging_mode: Literal[0, 1, 2]  # Logging Mode, allowed values are 0, 1, 2
    log_length: conint(ge=1, le=255)  # Log Length in minutes
    data_format: Literal[2, 3, 4, 130, 131, 132]  # Data Format


class SpectrumSetupReadModel(BaseModel):
    reference_level: conint(ge=0, le=100)  # Reference Level in dB relative to 1V
    sample_rate: Literal[
        1000, 2000, 4000, 8000, 16000, 32000, 64000, 128000, 256000, 512000
    ]  # Sample Rate in samples per second
    fft_processing_type: Literal[4, 5, 6]  # FFT Processing Type, allowed values are 0, 1, 2
    fft_accumulated: conint(ge=1, le=65535)  # FFT Accumulations
    fft_weighting_factor: conint(ge=1, le=65535)  # FFT Weighting Factor
    logging_mode: Literal[0, 1, 2]  # Logging Mode, allowed values are 0, 1, 2
    log_length: conint(ge=1, le=255)  # Log Length in minutes


class JobSetupReadModel(BaseModel):
    waveform_setup: Optional[WaveFormSetupReadModel]
    spectrum_setup: Optional[SpectrumSetupReadModel]
