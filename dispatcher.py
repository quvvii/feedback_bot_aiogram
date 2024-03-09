import logging
from aiogram import Bot, Dispatcher
from filters import IsAdminFilter, IsReplyFilter, IsUserFilter
from misc import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Configure logging
logging.basicConfig(level=logging.INFO)

# storage
storage = MemoryStorage()

# prerequisites
if not config.token:
    exit("No token provided")

# init
bot = Bot(token=config.token, parse_mode="HTML", disable_web_page_preview=True)
dp: Dispatcher = Dispatcher(bot, storage=storage)

# activate filters
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(IsReplyFilter)
dp.filters_factory.bind(IsUserFilter)