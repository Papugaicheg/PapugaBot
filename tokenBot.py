import logging

from aiogram import Bot, Dispatcher
bot = Bot(token="1751405813:AAGC2x1EGIJy1JSuMdnEF9tsFSsu9upQCVI")



# Объект бота

# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Запуск бота
