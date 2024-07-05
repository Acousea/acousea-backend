from core.shared.domain.address import Address, RequestType


# TODO: Add an argument to specify LORA_PACKET or IRIDIUM_PACKET
class CommunicationRequest:
    def __init__(self, command_code: chr, recipient_address: int, payload: bytes):
        self.sync_byte: bytes = b' '
        # Address byte: [Bits 7:6 -> Sender Addr, Bits 5:4 -> Rec. Addr]
        self.op_code: chr = command_code
        self.addresses: int = (Address.BACKEND << 6) | (recipient_address << 4) | RequestType.IRIDIUM_PACKET
        self.payload_length: int = len(payload)
        self.payload: bytes = payload

    @classmethod
    def reconstruct(cls, sync_byte: bytes, command_code: chr, sender_address: int, recipient_address: int, request_type: int, payload_length: int,
                    payload: bytes):
        instance = cls(command_code, recipient_address, payload)
        instance.sync_byte = sync_byte
        instance.op_code = command_code
        instance.addresses = (sender_address << 6) | (recipient_address << 4) | request_type
        instance.payload_length = payload_length
        instance.payload = payload
        return instance

    @classmethod
    def reconstruct_from_bytes(cls, request: bytes):
        sync_byte = request[0].to_bytes(1, byteorder='little')
        command_code = chr(request[1])
        addresses = request[2]
        sender_address = (addresses & Address.SENDER_MASK) >> 6
        recipient_address = (addresses & Address.RECEIVER_MASK) >> 4
        request_type = addresses & (RequestType.LORA_PACKET | RequestType.IRIDIUM_PACKET)
        payload_length = request[3]
        payload = request[4:]
        return cls.reconstruct(sync_byte, command_code, sender_address, recipient_address, request_type, payload_length, payload)

    def __str__(self):
        """Response in bytes"""
        return ('(0x' + ' 0x'.join(f'{byte:02X}' for byte in
                                   [ord(self.sync_byte), ord(self.op_code), self.addresses, self.payload_length] + list(
                                       self.payload)) + ')')

    def __repr__(self):
        return f"0x" + ' 0x'.join(f'{byte:02X}' for byte in
                                  [ord(self.sync_byte), ord(self.op_code), self.addresses, self.payload_length] + list(
                                      self.payload)) + ')'

    @property
    def sender_address(self):
        return (self.addresses & Address.SENDER_MASK) >> 6

    @property
    def recipient_address(self):
        return (self.addresses & Address.RECEIVER_MASK) >> 4

    @property
    def request_type(self):
        return self.addresses & (RequestType.LORA_PACKET | RequestType.IRIDIUM_PACKET)

    def is_recipient_address(self, address):
        return (self.addresses & Address.RECEIVER_MASK) == (address << 4)

    def set_as_lora_packet(self):
        self.addresses = (self.addresses & RequestType.CLEAN_PACKET_TYPE) | RequestType.LORA_PACKET

    def set_as_iridium_packet(self):
        self.addresses = (self.addresses & RequestType.CLEAN_PACKET_TYPE) | RequestType.IRIDIUM_PACKET

    def encode(self) -> bytes:
        """ Return the payload as bytes with the format
            byte[0] = space (sync byte)
            byte[1] = code
            byte[2] = addresses [Bits 7:6 -> Sender Addr, Bits 5:4 -> Rec. Addr]
            byte[3] = payload length
            byte[4...n] = payload
        """
        encoded_payload = (self.sync_byte + bytes([ord(self.op_code)]) + bytes([self.addresses]) +
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
        encoded_payload = (self.sync_byte + bytes([ord(self.op_code)]) + bytes([self.addresses]) +
                           bytes([self.payload_length]) + self.payload)
        return ''.join(f'{byte:02x}' for byte in encoded_payload)

    def get_payload(self) -> bytes:
        return self.payload
