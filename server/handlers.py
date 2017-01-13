from server.portal_work import Birthdays, CanNotAutorize
from models import Subscriber

import msg


def format_date(str_date):
    try:
        date = str_date.split('-')
        return '{}.{}'.format(date[2], date[1])
    except:
        return msg.DATE_ERROR


def generate_message(birthday_people, add_date):
    if len(birthday_people) < 1:
        return msg.NO_BIRTHDAYS
    result = ""
    try:
        if add_date:
            birthday_str = ['{} {} ({})'.format(man['first_name'], man['last_name'], format_date(man['birth_date']))
                            for man in birthday_people]
        else:
            birthday_str = ['{} {}'.format(man['first_name'], man['last_name']) for man in birthday_people]
        result += ', '.join(birthday_str)
        return result
    except:
        return msg.BIRTHDAYS_PARSE_ERROR


def start_handler(bot, update):
    bot.sendMessage(update.message.chat_id, text=msg.START)


def weekly_birthdays_handler(bot, update):
    try:
        birthday_people = Birthdays().get_weekly_birthdays()
        bot.sendMessage(update.message.chat_id, text=generate_message(birthday_people, True))
    except CanNotAutorize as e:
        bot.sendMessage(update.message.chat_id, text=e.message)


def today_birthdays_handler(bot, update):
    try:
        birthday_people = Birthdays().get_todays_birthdays()
        bot.sendMessage(update.message.chat_id, text=generate_message(birthday_people, False))
    except CanNotAutorize as e:
        bot.sendMessage(update.message.chat_id, text=e.message)



def unknown_command_handler(bot, update):
    bot.sendMessage(update.message.chat_id, text=msg.UNKNOWN_COMMAND)


def add_subscriber_handler(bot, update):
    sub, created = Subscriber.get_or_create(channel=update.message.chat_id)
    if created:
        bot.sendMessage(update.message.chat_id, text=msg.SUBSCRIPTION_SUCCESS)
    else:
        bot.sendMessage(update.message.chat_id, text=msg.SUBSCRIPTION_ALREADY_EXISTS)


def remove_subscriber_handler(bot, update):
    try:
        sub = Subscriber.get(channel=update.message.chat_id)
        sub.delete_instance()
        bot.sendMessage(update.message.chat_id, text=msg.UNSUBSCRIPTION_SUCCESS)
    except:
        bot.sendMessage(update.message.chat_id, text=msg.SUBSCRIPTION_NOT_FOUND)

