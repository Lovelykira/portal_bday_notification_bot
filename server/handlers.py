from server.portal_work import get_weekly_birthdays, get_todays_birthdays
from models import Subscriber


def format_date(str_date):
    try:
        date = str_date.split('-')
        return '{}.{}'.format(date[2], date[1])
    except:
        return 'unknown'


def generate_message(birthday_people, add_date):
    if len(birthday_people) < 1:
        return "Дни рождения не обнаружены :)"
    result = ""
    try:
        for man in birthday_people:
            result += man['first_name'] + " "
            result += man['last_name'] + " "
            if add_date:
                result += "({}) \n".format(format_date(man['birth_date']))
        return result
    except:
        return 'Произошла ошибка. Зайди на Портал и посмотри portal.light-it.net.'


def start_handler(bot, update):
    bot.sendMessage(update.message.chat_id, text='Привет! Используй /help чтобы посмотреть список команд.')


def weekly_birthdays_handler(bot, update):
    birthday_people = get_weekly_birthdays()
    bot.sendMessage(update.message.chat_id, text=generate_message(birthday_people, True))


def today_birthdays_handler(bot, update):
    birthday_people = get_todays_birthdays()
    bot.sendMessage(update.message.chat_id, text=generate_message(birthday_people, False))


def unknown_command_handler(bot, update):
    bot.sendMessage(update.message.chat_id, text="Что? Попробуй /help .")


def add_subscriber_handler(bot, update):
    sub, created = Subscriber.get_or_create(channel=update.message.chat_id)
    if created:
        bot.sendMessage(update.message.chat_id, text="Спасибо! Теперь вы подписаны на оповещения.")
    else:
        bot.sendMessage(update.message.chat_id, text="Вы уже подписаны на оповещения.")


def remove_subscriber_handler(bot, update):
    try:
        sub = Subscriber.get(channel=update.message.chat_id)
        sub.delete_instance()
        bot.sendMessage(update.message.chat_id, text="Вы отписались от оповещений.")
    except:
        bot.sendMessage(update.message.chat_id, text="Вы не подписаны на оповещения.")

