import struct
from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class DrifterSummaryReportResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        self.epoch_time: int = int.from_bytes(self.data[0:4], byteorder='little')

        # PAMDeviceStats
        pam_device_unit_status_battery_status: int = int.from_bytes(self.data[4:5], byteorder='little')
        self.pam_device_unit_status = pam_device_unit_status_battery_status & 0xF0
        self.pam_device_battery_status = pam_device_unit_status_battery_status & 0x0F
        self.pam_device_battery_percentage: int = int.from_bytes(self.data[5:6], byteorder='little')
        self.pam_device_temperature: int = int.from_bytes(self.data[6:7], byteorder='little')
        self.pam_device_humidity: int = int.from_bytes(self.data[7:8], byteorder='little')

        # DrifterModuleStats
        self.drifter_module_temperature: int = int.from_bytes(self.data[8:9], byteorder='little')
        self.drifter_module_battery_percentage: int = int.from_bytes(self.data[9:10], byteorder='little')
        battery_status_and_operation_mode: int = int.from_bytes(self.data[10:11], byteorder='little')
        self.drifter_module_operation_mode: int = battery_status_and_operation_mode & 0x0F
        self.drifter_module_battery_status: int = (battery_status_and_operation_mode >> 4) & 0x0F
        reserved = int.from_bytes(self.data[11:12], byteorder='little')
        self.latitude: float = struct.unpack('<f', self.data[12:16])[0]
        self.longitude: float = struct.unpack('<f', self.data[16:20])[0]
        self.drifter_module_storage_used: int = int.from_bytes(self.data[20:24], byteorder='little')
        self.drifter_module_storage_total: int = int.from_bytes(self.data[24:28], byteorder='little')

        # AudioDetectionStats
        self.audio_total_num_detections: int = int.from_bytes(self.data[28:30], byteorder='little')
        self.audio_recorded_minutes: int = int.from_bytes(self.data[30:32], byteorder='little')
        self.audio_processed_minutes: int = int.from_bytes(self.data[32:34], byteorder='little')
        self.audio_num_files: int = int.from_bytes(self.data[34:36], byteorder='little')

    def __str__(self):
        return (f"DrifterSummaryReportResponse("
                f"epoch_time={self.epoch_time}, "
                f"pam_device_unit_status={self.pam_device_unit_status}, "
                f"pam_device_battery_status={self.pam_device_battery_status}, "
                f"pam_device_battery_percentage={self.pam_device_battery_percentage}, "
                f"pam_device_temperature={self.pam_device_temperature}, "
                f"pam_device_humidity={self.pam_device_humidity}, "
                f"drifter_module_temperature={self.drifter_module_temperature}, "
                f"drifter_module_battery_percentage={self.drifter_module_battery_percentage}, "
                f"drifter_module_battery_status={self.drifter_module_battery_status}, "
                f"drifter_module_operation_mode={self.drifter_module_operation_mode}, "
                f"latitude={self.latitude}, "
                f"longitude={self.longitude}, "
                f"drifter_module_storage_used={self.drifter_module_storage_used}, "
                f"drifter_module_storage_total={self.drifter_module_storage_total}, "
                f"audio_total_num_detections={self.audio_total_num_detections}, "
                f"audio_recorded_minutes={self.audio_recorded_minutes}, "
                f"audio_processed_minutes={self.audio_processed_minutes}, "
                f"audio_num_files={self.audio_num_files})")

    def __repr__(self):
        return self.__str__()
