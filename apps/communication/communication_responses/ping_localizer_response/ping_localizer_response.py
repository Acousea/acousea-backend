from apps.communication.communication_responses.communication_response import CommunicationResponse


class PingLocalizerResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)

        # Throw exception if the data_length is not equal to the length of the data
        if self.data_length != len(self.data):
            raise ValueError("Data length does not match the length of the data")

    def __str__(self):
        return f'PingLocalizerResponse{super().__str__()}'

    def __repr__(self):
        return f'PingLocalizerResponse{super().__repr__()}'