from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
from time import sleep
from signal import signal, SIGINT, SIGTERM, SIGABRT

import server.handlers as handlers
import conf

from server.portal_work import get_todays_birthdays
from server.handlers import generate_message
from models import Subscriber



HANDLER_MAPPING = {
    'start': handlers.start_handler,
    'birthdays_week': handlers.weekly_birthdays_handler,
    'birthdays_today': handlers.today_birthdays_handler,
    'subscribe': handlers.add_subscriber_handler,
    'unsubscribe': handlers.remove_subscriber_handler,
}


def help_handler(bot, update):
    result_message = 'Доступные команды: '
    for command in HANDLER_MAPPING.keys():
        result_message += "/" + command + " "
    bot.sendMessage(update.message.chat_id, text=result_message)


class UpdaterNotificate(Updater):
    def idle(self, stop_signals=(SIGINT, SIGTERM, SIGABRT)):
        for sig in stop_signals:
            signal(sig, self.signal_handler)

        self.is_idle = True

        while self.is_idle:
            if datetime.datetime.now().time().hour == 16 and \
               datetime.datetime.now().time().minute == 39 and \
               datetime.datetime.now().time().second == 0:
                self.notificate()
            sleep(1)

    def notificate(self):
        subs = Subscriber.select()
        birthday_people = get_todays_birthdays()
        if len(birthday_people) > 0:
            for sub in subs:
                self.bot.sendMessage(sub.channel, text=self.generate_notification(birthday_people))

    def generate_notification(self, birthday_people):
        result = 'Сегодня День рождения празднуют: \n'
        try:
            for man in birthday_people:
                result += man['first_name'] + " "
                result += man['last_name'] + ", \n"
            return result[:-3]
        except:
            return 'Сегодня у кого-то День рождения, но из-за ошибки я не знаю у кого. Зайди на Портал и посмотри!'



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


