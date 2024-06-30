# services/rockblock_messages_repository.py
from typing import List, Tuple

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

    def get_all_messages_non_paginated(self) -> List[RockBlockMessage]:
        messages = self.db.query(SQLRockBlockMessage).all()
        return [message.to_rockblock_message() for message in messages]

    def get_all_messages_paginated(self, page: int, page_size: int) -> List[RockBlockMessage]:
        messages = self.db.query(SQLRockBlockMessage).limit(page_size).offset(page * page_size).all()
        return [message.to_rockblock_message() for message in messages]

    def get_messages_paginated(self, page: int, rows_per_page: int) -> Tuple[List[RockBlockMessage], int]:
        total = self.db.query(SQLRockBlockMessage).count()
        messages = (
            self.db.query(SQLRockBlockMessage)
            .offset((page - 1) * rows_per_page)
            .limit(rows_per_page)
            .all()
        )
        return [message.to_rockblock_message() for message in messages], total

    def get_messages_paginated_sorted_by_date(self, page: int, rows_per_page: int) -> Tuple[List[RockBlockMessage], int]:
        total = self.db.query(SQLRockBlockMessage).count()
        messages = (
            self.db.query(SQLRockBlockMessage)
            .order_by(SQLRockBlockMessage.transmit_time.desc())
            .offset((page - 1) * rows_per_page)
            .limit(rows_per_page)
            .all()
        )
        return [message.to_rockblock_message() for message in messages], total
