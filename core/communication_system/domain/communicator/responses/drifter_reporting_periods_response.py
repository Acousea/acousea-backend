from core.communication_system.domain.communicator.communication_response import CommunicationResponse

class DrifterReportingPeriodsResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)

        self.ack_nack = self.data[0]

        # Helper function to decode uint16 from little endian bytes
        def decode_from_little_endian(data, start_index):
            return int.from_bytes(data[start_index:start_index+2], 'little')

        self.launching_sbd_period = decode_from_little_endian(self.data, 1)
        self.launching_lora_period = decode_from_little_endian(self.data, 3)
        self.working_sbd_period = decode_from_little_endian(self.data, 5)
        self.working_lora_period = decode_from_little_endian(self.data, 7)
        self.recovering_sbd_period = decode_from_little_endian(self.data, 9)
        self.recovering_lora_period = decode_from_little_endian(self.data, 11)

    def __str__(self):
        return (f"DrifterReportingPeriodsResponse(ack_nack={self.ack_nack}, "
                f"launching_sbd_period={self.launching_sbd_period}, launching_lora_period={self.launching_lora_period}, "
                f"working_sbd_period={self.working_sbd_period}, working_lora_period={self.working_lora_period}, "
                f"recovering_sbd_period={self.recovering_sbd_period}, recovering_lora_period={self.recovering_lora_period})")

    def __repr__(self):
        return self.__str__()
