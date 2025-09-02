import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from random import choice

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Ваш токен бота. Он будет подставлен из переменной окружения!
TOKEN = os.getenv('BOT_TOKEN') # Очень важно! Код читает токен из переменной, а не из файла.

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = [['Камень 🪨', 'Ножницы ✂️', 'Бумага 📜']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Давай сыграем! Выбирай:",
        reply_markup=reply_markup
    )

# Обработчик ходов пользователя
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_choice = update.message.text
    bot_choice = choice(['Камень 🪨', 'Ножницы ✂️', 'Бумага 📜'])
    
    # Определяем победителя
    if user_choice == bot_choice:
        result = "Ничья! 🤝"
    elif (user_choice == 'Камень 🪨' and bot_choice == 'Ножницы ✂️') or \
         (user_choice == 'Ножницы ✂️' and bot_choice == 'Бумага 📜') or \
         (user_choice == 'Бумага 📜' and bot_choice == 'Камень 🪨'):
        result = "Ты выиграл! 🎉"
    else:
        result = "Я выиграл! 🤖"
    
    await update.message.reply_text(f"Твой выбор: {user_choice}\nМой выбор: {bot_choice}\n\n{result}")

def main():
    # Создаем Application
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('^(Камень 🪨|Ножницы ✂️|Бумага 📜)$'), play))
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
