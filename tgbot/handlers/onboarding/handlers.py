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
    feed_back_keyboard,
)
from tgbot import states
from tgbot.handlers.onboarding.static_text import CONTACT_KEYBOARD
from users.models import Settings


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if not u.language:
        text = "Tilni tanlang / Выберите язык"
        update.message.reply_text(text, reply_markup=language_keyboard())
        return states.LANGUAGE
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)
        update.message.reply_text(text=text, reply_markup=main_keyboard())


def choose_correct_lang(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    text = "Tilni tanlang / Выберите язык Quyidagilardan birini kiriting."
    update.message.reply_text(text, reply_markup=language_keyboard())
    return states.LANGUAGE


def choose_language(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if update.message.text == UZBEK:
        u.language = "uz"
    elif update.message.text == RUSSIAN:
        u.language = "ru"
    u.save()
    text = static_text.start_not_created.format(first_name=u.first_name)
    update.message.reply_text(text=text, reply_markup=main_keyboard())
    return states.MAIN


def contact_number(update: Update, context: CallbackContext):
    phone_number = Settings.phone_number
    if update.message.text == CONTACT_KEYBOARD:
        update.message.reply_text(text=phone_number)
    return states.MAIN


def give_feed_back(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        text="O'z fikr va mulohazalaringizni jo'nating.",
        reply_markup=feed_back_keyboard(),
    )
    return states.GET_FEEDBACK


def send_feed_back(update: Update, context: CallbackContext) -> int:
    u, created = User.get_user_and_created(update, context)
    result = update.message.text

    if u.feed_back == None:
        u.feed_back = result
        u.save()
    else:
        u.update_feed_back(result)
    update.message.reply_text(text=result, reply_markup=main_keyboard())
