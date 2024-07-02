from core.communication_system.domain.communicator.communication_response import CommunicationResponse


class ErrorCommunicationResponse(CommunicationResponse):
    def __init__(self, response: bytes):
        super().__init__(response)
        response_content = super().content()

        # Decodificación de la respuesta según el formato descrito
        self.error_code = response_content[0]

    def __str__(self):
        return (f"ErrorResponse("
                f"error_code={self.error_code}, "
                f"description={self.get_error_description()})")

    def __repr__(self):
        return str(self)

    def get_error_description(self) -> str:
        error_descriptions = {
            0x01: "Invalid Operation Code",
            0x02: "Invalid Payload",
            0x03: "Invalid Sender Address",
            0x04: "Invalid Receiver Address",
            0x05: "Invalid Packet Length",
            0x06: "Invalid Sync Byte",
            0x07: "Internal ICListen API Error",
        }
        return error_descriptions.get(self.error_code, "Unknown error code")
