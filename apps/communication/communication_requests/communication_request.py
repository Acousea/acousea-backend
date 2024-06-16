class CommunicationRequest:
    def __init__(self, command_code: str, payload: bytes):
        self.code: str = command_code
        self.payload_length: int = len(payload)
        self.payload: bytes = payload

    def __str__(self) -> str:
        return f'{self.code} {self.payload}\n'

    def encode(self) -> bytes:
        """ Return the payload as bytes with the format
            byte[0] = code
            byte[1] = space
            byte[2] = payload_length
            byte[3...n] = payload
        """
        encoded_payload = self.code.encode('utf-8') + b' ' + bytes([self.payload_length]) + self.payload + b'\n'
        return encoded_payload

    def get_payload(self) -> bytes:
        return self.payload
