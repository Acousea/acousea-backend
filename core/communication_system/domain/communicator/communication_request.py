from core.shared.domain.address import Address


# TODO: Add an argument to specify LORA_PACKET or IRIDIUM_PACKET
class CommunicationRequest:
    def __init__(self, command_code: str, recipient_address: int, payload: bytes, flush: bool = False):
        self.sync_byte: bytes = b' '
        # Address byte: [Bits 7:6 -> Sender Addr, Bits 5:4 -> Rec. Addr]
        self.code: str = command_code
        self.addresses: int = (Address.BACKEND << 6) | (recipient_address << 4) | Address.LORA_PACKET
        self.payload_length: int = len(payload)
        self.payload: bytes = payload
        self.flush: bool = flush

    def __str__(self):
        """Response in bytes"""
        return ('(' + ' '.join(f'{byte:02x}' for byte in
                               [ord(self.sync_byte), ord(self.code), self.addresses, self.payload_length] + list(
                                   self.payload)) + ')')

    def __repr__(self):
        return f"({self.sync_byte}, {self.code}, {self.addresses}, {self.payload_length}, {self.payload})"

    def is_recipient_address(self, address):
        return (self.addresses & Address.RECEIVER_MASK) == (address << 4)

    def set_lora_packet(self):
        self.addresses = (self.addresses & Address.CLEAN_PACKET_TYPE) | Address.LORA_PACKET

    def set_iridium_packet(self):
        self.addresses = (self.addresses & Address.CLEAN_PACKET_TYPE) | Address.IRIDIUM_PACKET

    def encode(self) -> bytes:
        """ Return the payload as bytes with the format
            byte[0] = space (sync byte)
            byte[1] = code
            byte[2] = addresses [Bits 7:6 -> Sender Addr, Bits 5:4 -> Rec. Addr]
            byte[3] = payload length
            byte[4...n] = payload
        """
        encoded_payload = (self.sync_byte + bytes([ord(self.code)]) + bytes([self.addresses]) +
                           bytes([self.payload_length]) + self.payload)
        return encoded_payload

    def encode_str(self) -> str:
        """ Return the payload as bytes with the format
            byte[0] = space (sync byte)
            byte[1] = code
            byte[2] = addresses [Bits 7:6 -> Sender Addr, Bits 5:4 -> Rec. Addr]
            byte[3] = payload length
            byte[4...n] = payload
        """
        encoded_payload = (self.sync_byte + bytes([ord(self.code)]) + bytes([self.addresses]) +
                           bytes([self.payload_length]) + self.payload)
        return ''.join(f'{byte:02x}' for byte in encoded_payload)

    def get_payload(self) -> bytes:
        return self.payload
