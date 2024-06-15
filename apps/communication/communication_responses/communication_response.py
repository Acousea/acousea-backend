class CommunicationResponse:
    def __init__(self, response: bytes):
        self.response = response

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
