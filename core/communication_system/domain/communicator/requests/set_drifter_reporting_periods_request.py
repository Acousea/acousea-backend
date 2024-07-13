from core.communication_system.domain.communicator.communication_request import CommunicationRequest
from core.communication_system.domain.reporting_periods import ReportingPeriods
from core.shared.domain.address import Address
from core.shared.domain.operation_codes import OperationCode


class SetDrifterReportingPeriodsRequest(CommunicationRequest):
    def __init__(self, reporting_periods: ReportingPeriods):
        payload = self.encode_payload(reporting_periods)
        super().__init__(OperationCode.SET_REPORTING_PERIODS, Address.DRIFTER, payload)

    @staticmethod
    def encode_payload(reporting_periods: ReportingPeriods) -> bytes:
        # Helper function to encode a uint16 value to little endian
        def encode_to_little_endian(value):
            return [value & 0xFF, (value >> 8) & 0xFF]

        payload = []
        payload.extend(encode_to_little_endian(reporting_periods.launchingSbdPeriod))
        payload.extend(encode_to_little_endian(reporting_periods.launchingLoraPeriod))
        payload.extend(encode_to_little_endian(reporting_periods.workingSbdPeriod))
        payload.extend(encode_to_little_endian(reporting_periods.workingLoraPeriod))
        payload.extend(encode_to_little_endian(reporting_periods.recoveringSbdPeriod))
        payload.extend(encode_to_little_endian(reporting_periods.recoveringLoraPeriod))

        return bytes(payload)

    def __str__(self):
        return (f'SetDrifterReportingPeriodsRequest( '
                f'launching_sbd_period={int.from_bytes(self.payload[0:2], "little")}, '
                f'launching_lora_period={int.from_bytes(self.payload[2:4], "little")}, '
                f'working_sbd_period={int.from_bytes(self.payload[4:6], "little")}, '
                f'working_lora_period={int.from_bytes(self.payload[6:8], "little")}, '
                f'recovering_sbd_period={int.from_bytes(self.payload[8:10], "little")}, '
                f'recovering_lora_period={int.from_bytes(self.payload[10:12], "little")})')

    def __repr__(self):
        return self.__str__()
