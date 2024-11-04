import os  # Стандартная библиотека
from dotenv import load_dotenv  # Сторонняя библиотека
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update  # Сторонняя библиотека
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes  # Сторонняя библиотека

# Загружаем переменные окружения из .env файла
load_dotenv()

if __name__ == '__main__':
    application = (
        ApplicationBuilder()
        .token("7543357838:AAHakopJhfsdaSNzW4xKP9qg7ifwsqWaQG0")  # Замените на токен вашего бота
        .build()
    )

    # Список продуктов по категориям
    PRODUCTS = {
        "Аниме": ["Фигурки", "Плакаты", "Манга"],
        "Игры": ["PlayStation", "Xbox", "ПК игры"],
        "Косплей": ["Костюмы", "Аксессуары"],
        "Детали": ["Запчасти для ПК", "Мониторы"],
        "Под заказ": ["Специальные товары", "Эксклюзивы"]
    }

    # Команда /start
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Создаем кнопку "Каталог"
        keyboard = [[InlineKeyboardButton("Каталог", callback_data='catalog')]]
        
        # Отправляем сообщение с кнопкой
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Добро пожаловать! Нажмите "Каталог", чтобы посмотреть доступные продукты.', reply_markup=reply_markup)

    # Обработчик нажатия на кнопку "Каталог"
    async def catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()  # Уведомляем Telegram, что запрос обработан
        
        # Создаем клавиатуру с категориями продуктов
        keyboard = [
            [InlineKeyboardButton(category, callback_data=category) for category in PRODUCTS.keys()]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text('Выберите категорию:', reply_markup=reply_markup)

    # Обработчик нажатий на категории
    async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()  # Уведомляем Telegram, что запрос обработан
        
        category = query.data  # Получаем название категории
        products_list = PRODUCTS[category]  # Получаем список продуктов для выбранной категории
        
        # Формируем сообщение с продуктами
        products_message = f"Продукты в категории '{category}':\n" + "\n".join(products_list)
        
        await query.edit_message_text(products_message)

    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(catalog, pattern='catalog'))
    application.add_handler(CallbackQueryHandler(show_products, pattern='^(Аниме|Игры|Косплей|Детали|Под заказ)$'))

    # Запускаем бота
    application.run_polling()
