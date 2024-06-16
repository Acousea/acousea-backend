from apps.communication.communication_responses.communication_response import CommunicationResponse


class PingDrifterResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        self.opcode = response[0]
        self.data_length = response[2]
        self.data = response[3:-1]

        # Throw exception if the data_length is not equal to the length of the data
        if self.data_length != len(self.data):
            raise ValueError("Data length does not match the length of the data")

