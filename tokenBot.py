import logging

from aiogram import Bot, Dispatcher
bot = Bot(token="")



# Объект бота

# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Запуск бота
