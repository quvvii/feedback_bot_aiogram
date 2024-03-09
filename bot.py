from aiogram import executor
import tracemalloc, os

from dispatcher import dp

import handlers

tracemalloc.start()

# start bot
if __name__ == "__main__":
    os.system('clear' if os.name != 'nt' else 'cls')
    executor.start_polling(dp, skip_updates=True)