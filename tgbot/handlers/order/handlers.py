import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import (
    UZBEK,
    RUSSIAN,
    main_keyboard,
    language_keyboard,
)
from tgbot import states
from product.models import Product, Category

from telegram import ReplyKeyboardMarkup


def category(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)
    categories = Category.objects.filter(parent=None)
    if not len(categories):
        update.message.reply_text("No categories")
        
    keyboard = []
    for index in range(0, len(categories), 2):
        if len(categories) - 1 == index:
            keyboard.append([categories[index].title])
        else:
            keyboard.append([categories[index].title, categories[index + 1].title])

    update.message.reply_text("Keyboard", reply_markup=ReplyKeyboardMarkup(keyboard))



