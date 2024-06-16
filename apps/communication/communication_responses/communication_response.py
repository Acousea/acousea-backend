class CommunicationResponse:
    def __init__(self, response: bytes):
        self.response = response
        if response is None or len(response) == 0:
            return
        self.opcode = response[0]
        self.data_length = response[2]
        self.data = response[3:-1]

        print("Response:", response)
        # Throw exception if the data_length is not equal to the length of the data
        if self.data_length != len(self.data):
            raise ValueError("Data length does not match the length of the data: Specified length: %d, Real Data length: %d",
                             self.data_length, len(self.data))

    def __str__(self):
        """Response in bytes"""
        return ' '.join(f'{byte:02x}' for byte in self.response)
        # return ' '.join(str(byte) for byte in self.response)

    def __repr__(self):
        return f"Communication({self.response})"

    def __eq__(self, other):
        return self.response == other.response

    def empty(self):
        return self.response is None or len(self.response) == 0

    def content(self):
        return self.response[3:-1]
