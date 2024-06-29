from datetime import datetime, timedelta
from random import Random

from core.communication_system.domain.rockblock_message import RockBlockMessage


class RockBlockMessageMother:
    @staticmethod
    def create() -> RockBlockMessage:
        random = Random()
        return RockBlockMessage(
            imei="300234010753370",
            serial="12345",
            momsn=random.randint(0, 65535),
            transmit_time= (datetime.utcnow() - timedelta(days=random.randint(0, 365))).isoformat() + 'Z',
            iridium_latitude=random.uniform(-90, 90),
            iridium_longitude=random.uniform(-180, 180),
            iridium_cep=random.randint(1, 10),
            data=RockBlockMessageMother.get_random_data()
        )

    @staticmethod
    def get_random_data() -> str:
        random = Random()
        return ''.join([random.choice('0123456789abcdef') for _ in range(0, 100)])


if __name__ == '__main__':
    print(RockBlockMessageMother.create())
