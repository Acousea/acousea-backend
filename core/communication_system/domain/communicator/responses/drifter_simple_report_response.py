import struct

from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class DrifterSimpleReportResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        self.epoch_time: int = int.from_bytes(self.data[0:4], byteorder='little')
        self.battery_percentage: int = int.from_bytes(self.data[4:5], byteorder='little')
        self.battery_status: int = int.from_bytes(self.data[5:6], byteorder='little')
        self.latitude: float = struct.unpack('<f', self.data[6:10])[0]
        self.longitude: float = struct.unpack('<f', self.data[10:14])[0]
        self.operation_mode: int = int.from_bytes(self.data[14:15], byteorder='little')
        self.temperature: int = int.from_bytes(self.data[15:16], byteorder='little')
        self.storage_free: int = int.from_bytes(self.data[16:20], byteorder='little')
        self.storage_total: int = int.from_bytes(self.data[20:24], byteorder='little')

    def __str__(self):
        return (f"DrifterSimpleReportResponse("
                f"epoch_time={self.epoch_time}, "
                f"battery_percentage={self.battery_percentage}, "
                f"battery_status={self.battery_status}, "
                f"latitude={self.latitude}, "
                f"longitude={self.longitude}, "
                f"operation_mode={self.operation_mode}, "
                f"temperature={self.temperature}, "
                f"storage_free={self.storage_free}, "
                f"storage_total={self.storage_total})")

    def __repr__(self):
        return self.__str__()
