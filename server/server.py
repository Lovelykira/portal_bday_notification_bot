from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
from time import sleep
from signal import signal, SIGINT, SIGTERM, SIGABRT

import server.handlers as handlers
import conf

import msg
from server.notification_service import NotificationService
from server.notifications.birthday_notification import BirthdayNotification


HANDLER_MAPPING = {
    'start': handlers.start_handler,
    'birthdays_week': handlers.weekly_birthdays_handler,
    'birthdays_today': handlers.today_birthdays_handler,
    'subscribe': handlers.add_subscriber_handler,
    'unsubscribe': handlers.remove_subscriber_handler,
}


def help_handler(bot, update):
    commands_str = ', \n'.join(['/{}'.format(command) for command in sorted(HANDLER_MAPPING.keys())])
    result_message = msg.AVAILABLE_COMMANDS.format(commands_str)
    bot.sendMessage(update.message.chat_id, text=result_message)


class UpdaterNotificate(Updater):

    def idle(self, stop_signals=(SIGINT, SIGTERM, SIGABRT)):
        for sig in stop_signals:
            signal(sig, self.signal_handler)

        self.is_idle = True

        while self.is_idle:
            NotificationService().call_current_time_notifications(self.bot)
            sleep(1)


class BotServer:

    def run(self):
        updater = UpdaterNotificate(conf.BOT_TOKEN)
        dp = updater.dispatcher

        self.add_handlers(dp)
        updater.start_polling()
        updater.idle()

    def add_handlers(self, dp):
        for handler in HANDLER_MAPPING:
            dp.add_handler(CommandHandler(handler, HANDLER_MAPPING.get(handler)))

        dp.add_handler(CommandHandler('help', help_handler))
        dp.add_handler(MessageHandler(Filters.command, handlers.unknown_command_handler))


