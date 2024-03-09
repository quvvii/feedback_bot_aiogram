from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from misc import config


class IsAdminFilter(BoundFilter):
    """
    Custom filter "is_admin".
    """
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message):
        return message.from_user.id == int(config.admin_id)
    
class IsUserFilter(BoundFilter):
    """
    Custom filter "is_user".
    """
    key = "is_user"

    def __init__(self, is_user):
        self.is_user = is_user

    async def check(self, message: types.Message):
        return message.from_user.id != int(config.admin_id)
    
class IsReplyFilter(BoundFilter):
    """
    Custom filter "reply_to_message".
    """
    key = "reply_to_message"

    def __init__(self, reply_to_message):
        self.reply_to_message = reply_to_message

    async def check(self, message: types.Message):
        return message.reply_to_message and not message.from_user.is_bot
