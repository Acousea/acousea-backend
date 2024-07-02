import struct

from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class LocalizerSimpleReportResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        self.epoch_time: int = int.from_bytes(self.data[0:4], byteorder='little')
        self.battery_percent: int = int.from_bytes(self.data[4:5], byteorder='little')
        self.latitude: float = struct.unpack('<f', self.data[5:9])[0]
        self.longitude: float = struct.unpack('<f', self.data[9:13])[0]
        self.operation_mode: int = int.from_bytes(self.data[13:14], byteorder='little')

    def __str__(self):
        return (f'LocalizerDeviceInfoResponse (epoch_time={self.epoch_time}, '
                f'battery_percent={self.battery_percent}, latitude={self.latitude},'
                f'longitude={self.longitude},operation_mode = {self.operation_mode})')

    def __repr__(self):
        return self.__str__()
