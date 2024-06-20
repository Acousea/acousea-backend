class CommunicationResponse:
    def __init__(self, response: bytes):
        self.response: bytes = response
        if response is None or len(response) == 0:
            return
        self.sync_byte: int = response[0]
        self.__addresses: int = response[1]
        # Extraer senderAddress y recipientAddress del byte address
        self.sender_address: int = (self.__addresses & 0xC0) >> 6
        self.recipient_address: int = (self.__addresses & 0x30) >> 4

        self.opcode: int = response[2]
        self.data_length: int = response[3]
        self.data: bytes = response[4:]

        # Throw exception if the data_length is not equal to the length of the data
        if self.data_length != len(self.data):
            raise ValueError(f"Data length does not match the length of the data:"
                             f" Specified length: {self.data_length}, Actual length: {len(self.data)}")

    def __str__(self):
        """Response in bytes"""
        return '(' + ' '.join(f'{byte:02x}' for byte in self.response) + ')'

    def __repr__(self):
        return f"({self.response})"

    def __eq__(self, other):
        return self.response == other.response

    def empty(self):
        return self.response is None or len(self.response) == 0

    def content(self):
        return self.data
