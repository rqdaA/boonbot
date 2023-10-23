from typing import List


class Config:
    guild_id: int = -1

    bot_channel_id: int = -1
    main_channel_name: str = ""
    contests_category_id: int = 1166000686975172690

    member_role_ids: List[int] = []
    bot_role_ids: List[int] = []
    special_category_ids: List[int] = []


config = Config()
