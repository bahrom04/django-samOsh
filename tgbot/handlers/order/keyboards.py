from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON

from tgbot.handlers.onboarding import static_text


UZBEK = "🇺🇿 O'zbekcha"
RUSSIAN = "🇷🇺 Русский"


def language_keyboard() -> InlineKeyboardMarkup:
    buttons = [[UZBEK, RUSSIAN]]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [static_text.CONTACT_KEYBOARD, static_text.ORDER_KEYBOARD],
        [static_text.REVIEW_KEYBOARD, static_text.SETTINGS_KEYBOARD],
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)



