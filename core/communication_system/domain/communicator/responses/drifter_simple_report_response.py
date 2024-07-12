import struct

from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class DrifterSimpleReportResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        self.epoch_time: int = int.from_bytes(self.data[0:4], byteorder='little')
        self.latitude: float = struct.unpack('<f', self.data[4:8])[0]
        self.longitude: float = struct.unpack('<f', self.data[8:12])[0]
        self.battery_percentage: int = int.from_bytes(self.data[12:13], byteorder='little')
        battery_status_and_operation_mode: int = int.from_bytes(self.data[13:14], byteorder='little')
        self.battery_status: int = (battery_status_and_operation_mode >> 4) & 0x0F
        self.operation_mode: int = battery_status_and_operation_mode & 0x0F

    def __str__(self):
        return (f"DrifterSimpleReportResponse("
                f"epoch_time={self.epoch_time}, "
                f"battery_percentage={self.battery_percentage}, "
                f"battery_status={self.battery_status}, "
                f"latitude={self.latitude}, "
                f"longitude={self.longitude}, "
                f"operation_mode={self.operation_mode})")

    def __repr__(self):
        return self.__str__()
