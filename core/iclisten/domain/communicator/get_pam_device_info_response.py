import struct

from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class GetPAMDeviceInfoCommunicationResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        response_content = super().content()

        # Decodificación de la respuesta según el formato descrito
        self.unit_status = response_content[0]
        self.battery_status = response_content[1]
        self.battery_percentage = self._bytes_to_float(response_content[2:6])

        self.temperature = self._bytes_to_float(response_content[6:10])
        self.humidity = self._bytes_to_float(response_content[10:14])

    @staticmethod
    def _bytes_to_float(bytes_seq: bytes):
        return struct.unpack('f', bytes_seq)[0]

    def __str__(self):
        return (f"GetPAMDeviceInfoCommunicationResponse(unit_status={self.unit_status}, battery_status={self.battery_status},"
                f" battery_percentage={self.battery_percentage}, temperature={self.temperature}, humidity={self.humidity})")
