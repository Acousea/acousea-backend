from apps.communication.communication_responses.communication_response import CommunicationResponse


class ErrorResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        response_content = super().content()

        # Decodificación de la respuesta según el formato descrito
        self.error_code = response_content[0]

    def __str__(self):
        return (f"ErrorResponse("
                f"error_code={self.error_code}, "
                f"description={self.__error_description()})")

    def __repr__(self):
        return str(self)

    def __error_description(self):
        error_descriptions = {
            0x01: "INVALID_OPCODE",
            0x02: "INVALID_PAYLOAD",
            0x03: "INVALID_SENDER_ADDRESS",
            0x04: "INVALID_RECIPIENT_ADDRESS",
            0x05: "INVALID_PACKET_LENGTH",
            0x06: "INVALID_SYNC_BYTE",
            0x07: "INTERNAL_SERVER_ERROR",
        }
        return error_descriptions.get(self.error_code, "UNKNOWN_ERROR")
