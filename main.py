from aiogram.utils import executor
from handlers import dp


async def on_start(_):
    print('Бот стартовал!')


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_start)
