# services/rockblock_messages_repository.py
from typing import List

from sqlalchemy.orm import Session

from core.communication_system.domain.rockblock_message import RockBlockMessage
from core.communication_system.domain.sqlalchemy.sql_rockblock_messages import SQLRockBlockMessage


class RockBlockMessagesRepository:
    def __init__(self, db: Session):
        self.db = db

    def store_message(self, rock_block_message: RockBlockMessage) -> RockBlockMessage:
        db_packet = SQLRockBlockMessage.from_rockblock_message(rock_block_message)
        self.db.add(db_packet)
        self.db.commit()
        self.db.refresh(db_packet)
        return rock_block_message

    def get_messages(self) -> List[RockBlockMessage]:
        messages = self.db.query(SQLRockBlockMessage).all()
        return [message.to_rockblock_message() for message in messages]
