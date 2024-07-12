from core.communication_system.domain.communicator.responses.drifter_summary_report_response import DrifterSummaryReportResponse
from core.iclisten.application.ports.iclisten_repository import PAMSystemRepository
from core.iclisten.domain.communicator.get_pam_device_info_response import GetPAMDeviceInfoCommunicationResponse
from core.iclisten.domain.communicator.get_pam_device_streaming_config_response import GetPAMDeviceStreamingConfigCommunicationResponse
from core.iclisten.domain.communicator.set_pam_device_streaming_config_response import SetPAMDeviceStreamingConfigCommunicationResponse
from core.iclisten.domain.pam_system_logging_config_read_model import PAMDeviceLoggingConfigReadModel, PAMDeviceWaveformLoggingConfigReadModel, \
    PAMDeviceFFTLoggingConfigReadModel
from core.iclisten.domain.pam_system_status_info_read_model import PAMDeviceStatusReadModel
from core.iclisten.domain.pam_system_streaming_config_read_model import PAMDeviceStreamingConfigReadModel, PAMDeviceWaveformStreamingConfig, \
    PAMDeviceFFTStreamingConfig
from core.iclisten.domain.recording_stats_read_model import RecordingStatsReadModel


class MockPAMSystemRepository(PAMSystemRepository):
    def get_pam_device_status_info(self) -> PAMDeviceStatusReadModel:
        pam_device_status = PAMDeviceStatusReadModel(
            unit_status=2,
            battery_status=1,
            battery_percentage=99.0,
            temperature=29,
            humidity=32

        )
        return pam_device_status

    def get_logging_config(self) -> PAMDeviceLoggingConfigReadModel:
        waveform_logging_config = PAMDeviceWaveformLoggingConfigReadModel(
            log_waveform=True,
            gain=30,
            sample_rate=16000,
            logging_mode="Active",
            log_length=60,
            bit_depth=16,
            endianness="Little Endian"
        )

        fft_logging_config = PAMDeviceFFTLoggingConfigReadModel(
            log_fft=True,
            reference_level=10,
            sample_rate=16000,
            points_per_fft=1024,
            fft_processing_type="Mean Average",
            samples_between_ffts=512,
            ffts_accumulated=10,
            fft_weighting_factor=5,
            logging_mode="Active",
            log_length=60
        )

        logging_config = PAMDeviceLoggingConfigReadModel(
            timestamp="2024-07-08 12:34:56",
            waveform_config=waveform_logging_config,
            fft_config=fft_logging_config
        )

        return logging_config

    def get_streaming_config(self) -> PAMDeviceStreamingConfigReadModel:
        # Mock data for streaming config
        waveform_streaming_config = PAMDeviceWaveformStreamingConfig(
            record_waveform=True,
            process_waveform=True,
            waveform_processing_type=0,
            waveform_interval=512,
            waveform_duration=10
        )

        fft_streaming_config = PAMDeviceWaveformStreamingConfig(
            record_waveform=True,
            process_waveform=True,
            waveform_processing_type=0,
            waveform_interval=512,
            waveform_duration=10
        )

        streaming_config = PAMDeviceStreamingConfigReadModel(
            timestamp="2024-07-08 12:34:56",
            waveform_config=waveform_streaming_config,
            fft_config=fft_streaming_config
        )

        return streaming_config

    def get_latest_recording_stats(self, limit: int = 5) -> RecordingStatsReadModel:
        # Mock data for recording stats
        datetime_clicks = [
            {"datetime": 1625152800, "num_clicks": 1000},
            {"datetime": 1625156400, "num_clicks": 1500},
            {"datetime": 1625160000, "num_clicks": 1200},
            {"datetime": 1625163600, "num_clicks": 1300},
            {"datetime": 1625167200, "num_clicks": 1600}
        ]
        total_num_clicks = sum(click["num_clicks"] for click in datetime_clicks)
        total_recorded_minutes = 500
        total_number_of_files = 25

        return RecordingStatsReadModel(
            datetime_clicks=datetime_clicks,
            total_num_clicks=int(total_num_clicks),
            total_recorded_minutes=int(total_recorded_minutes),
            total_number_of_files=int(total_number_of_files)
        )

    def add_pam_device_status_info(self, device_info: GetPAMDeviceInfoCommunicationResponse) -> None:
        # This is a mock method, so we don't need to store anything.
        pass

    def add_recording_stats_info(self, drifter_summary_report_response: DrifterSummaryReportResponse):
        pass

    def update_pam_device_status_info(self, drifter_summary_report_response: DrifterSummaryReportResponse):
        pass

    def add_pam_device_streaming_config(self, pam_device_streaming_config: GetPAMDeviceStreamingConfigCommunicationResponse | SetPAMDeviceStreamingConfigCommunicationResponse):
        pass

