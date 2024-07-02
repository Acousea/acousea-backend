from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class PingRaspberryResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)

        # Throw exception if the data_length is not equal to the length of the data
        if self.data_length != len(self.data):
            raise ValueError("Data length does not match the length of the data")

    def __str__(self):
        """Extend the __str__ method to add extra content before and after the super class's __str__ output."""
        return f"PingRaspberryResponse{super().__str__()}"

    def __repr__(self):
        """Extend the __repr__ method to add extra content before and after the super class's __repr__ output."""
        return f"PingRaspberryResponse{super().__repr__()}"
