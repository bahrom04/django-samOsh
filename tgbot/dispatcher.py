"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.order import handlers as order_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.main import bot
from tgbot import states
from tgbot.handlers.onboarding.keyboards import UZBEK, RUSSIAN
from tgbot.handlers.onboarding import static_text


def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", onboarding_handlers.command_start),
            MessageHandler(
                Filters.text(static_text.ORDER_KEYBOARD),
                order_handlers.category,
            ),
            MessageHandler(
                Filters.text(static_text.REVIEW_KEYBOARD),
                onboarding_handlers.give_feed_back,
            ),
        ],
        states={
            states.LANGUAGE: [
                MessageHandler(
                    Filters.regex(f"^({UZBEK}|{RUSSIAN})$"),
                    onboarding_handlers.choose_language,
                ),
                MessageHandler(
                    Filters.all,
                    onboarding_handlers.choose_correct_lang,
                ),
            ],
            states.MAIN: [
                MessageHandler(
                    Filters.text,
                    order_handlers.category,
                ),
            ],
            states.FEEDBACK: [
                MessageHandler(
                    Filters.text,
                    onboarding_handlers.give_feed_back,
                )
            ],
            states.GET_FEEDBACK: [
                MessageHandler(
                    Filters.text,
                    onboarding_handlers.send_feed_back
                )
            ]
        },
        fallbacks=[
            CommandHandler("start", onboarding_handlers.command_start),
            MessageHandler(
                Filters.text(static_text.ORDER_KEYBOARD),
                order_handlers.category,
            ),
        ],
    )
    dp.add_handler(conv)
    # onboarding

    # admin commands
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    dp.add_handler(CommandHandler("export_users", admin_handlers.export_users))

    # broadcast message
    dp.add_handler(
        MessageHandler(
            Filters.regex(rf"^{broadcast_command}(/s)?.*"),
            broadcast_handlers.broadcast_command_with_message,
        )
    )
    dp.add_handler(
        CallbackQueryHandler(
            broadcast_handlers.broadcast_decision_handler,
            pattern=f"^{CONFIRM_DECLINE_BROADCAST}",
        )
    )

    # files
    dp.add_handler(
        MessageHandler(
            Filters.animation,
            files.show_file_id,
        )
    )

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(
    Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True)
)
