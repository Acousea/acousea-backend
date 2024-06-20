from apps.communication.communicator.address import Address


class CommunicationRequest:
    def __init__(self, command_code: str, recipient_address: int, payload: bytes):
        self.sync_byte: bytes = b' '
        # Address byte: [Bits 7:6 -> Sender Addr, Bits 5:4 -> Rec. Addr]
        self.addresses: int = (Address.BACKEND << 6) | (recipient_address << 4)
        print("Recipient address: ", recipient_address)
        print(f"-------------addresses: \\x{self.addresses:02x}")
        self.code: str = command_code
        self.payload_length: int = len(payload)
        self.payload: bytes = payload

    def __str__(self):
        """Response in bytes"""
        return ('(' + ' '.join(f'{byte:02x}' for byte in
                               [ord(self.sync_byte), self.addresses, ord(self.code), self.payload_length] + list(
                                   self.payload)) + ')')

    def __repr__(self):
        return f"({self.sync_byte}, {self.addresses}, {self.code}, {self.payload_length}, {self.payload})"

    def encode(self) -> bytes:
        """ Return the payload as bytes with the format
            byte[0] = space (sync byte)
            byte[1] = addresses [Bits 7:6 -> Sender Addr, Bits 5:4 -> Rec. Addr]
            byte[2] = code
            byte[3] = payload length
            byte[4...n] = payload
        """
        encoded_payload = (self.sync_byte + bytes(self.addresses) + bytes([int(self.code)]) +
                           bytes([self.payload_length]) + self.payload)
        return encoded_payload

    def get_payload(self) -> bytes:
        return self.payload
