from server.portal_work import Birthdays, CanNotAutorize
from models import Subscriber, SubscriberNotification

from server.notification_service import NotificationService

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


class DBHandler:
    """
    Handles database requests
    """
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def get_user_subscriptions(self):
        subscriber_notifications = SubscriberNotification.select().where(
            SubscriberNotification.subscriber == self.get_or_create_subscriber())
        return self._get_notification_names(subscriber_notifications)

    def get_or_create_subscriber(self):
        self._subscriber, _ = Subscriber.get_or_create(channel=self.chat_id)
        return self._subscriber

    def _get_notification_names(self, subscriber_notifications):
        notification_names = []
        for notification in subscriber_notifications:
            notification_names.append(notification.notification_name)
        return notification_names

    def subscribe_user(self, notification_name):
        SubscriberNotification.create(notification_name=notification_name, subscriber=self._subscriber)

    def delete_subscription(self, notification_name):
        SubscriberNotification.delete().where(
            SubscriberNotification.subscriber == self._subscriber,
            SubscriberNotification.notification_name == notification_name
        ).execute()


class SubscriptionHandler:
    """
    Helps to handle subscription messages
    """
    def __init__(self, update):
        self.update = update
        self.requested_subscription_names = self._text_to_list()
        self.notification_info = {}
        self.message = ''
        self.db_handler = DBHandler(self.update.message.chat_id)
        self.all_subscriptions = NotificationService.get_subscriptions()

    def subscribe(self):
        current_user_subscriptions = self.db_handler.get_user_subscriptions()

        if not self.requested_subscription_names:
            return self._show_info(self._get_available_subscriptions(current_user_subscriptions),
                                   msg.AVAILABLE_SUBSCRIPTIONS)

        for key in self.requested_subscription_names:
            if key in self.all_subscriptions:
                if key in current_user_subscriptions:
                    self._put_notification(msg.ALREADY_SUBSCRIBED_KEY, key)
                else:
                    self.db_handler.subscribe_user(key)
                    self._put_notification(msg.NEW_SUBSCRIPTION_KEY, key)
            else:
                self._put_notification(msg.UNKNOWN_SUBSCRIPTION_KEY, key)

        self._generate_message()
        return self.message

    def _show_info(self, subscriptions, template):
        formated_list = self._get_subscription_descriptions(subscriptions)
        return template.format(''.join(formated_list))

    def _get_subscription_descriptions(self, subscriptions):
        all_subscriptions = NotificationService.get_notifications_description('all')
        formated_list = []
        for sub in subscriptions:
            if sub in all_subscriptions.keys():
                formated_list.append('{} - {}'.format(sub, all_subscriptions[sub]))
        return formated_list

    def _get_available_subscriptions(self, current_user_subscriptions):
        all_subscriptions = NotificationService.get_notifications_description('all')
        available_subscriptions = []
        for sub in all_subscriptions.keys():
            if sub not in current_user_subscriptions:
                available_subscriptions.append(sub)
        return available_subscriptions

    def unsubscribe(self):
        current_user_subscriptions = self.db_handler.get_user_subscriptions()

        if not self.requested_subscription_names:
            return self._show_info(current_user_subscriptions, msg.AVAILABLE_UNSUBSCRIPTIONS)

        for key in self.requested_subscription_names:
            if key in self.all_subscriptions:
                if key in current_user_subscriptions:
                    self.db_handler.delete_subscription(key)
                    self._put_notification(msg.UNSUBSCRIPTION_KEY, key)
                else:
                    self._put_notification(msg.UNSUBSCRIPTION_ERROR_KEY, key)
            else:
                self._put_notification(msg.UNKNOWN_SUBSCRIPTION_KEY, key)

        self._generate_message()
        return self.message

    def _generate_message(self):
        for type, names in sorted(self.notification_info.items()):
            self._append_message(names, type)

    def _append_message(self, names, type):
        self.message += msg.SUBSCRIPTION_INFO[type].format(' '.join(names))

    def _put_notification(self, type, name):
        self.notification_info[type] = self.notification_info.get(type, [])
        self.notification_info[type].append(name)

    def _text_to_list(self):
        arguments = self.update.message.text.split(' ')
        return [] if len(arguments) == 1 else arguments[1:]


def add_subscriber_handler(bot, update):
    message = SubscriptionHandler(update=update).subscribe()
    bot.sendMessage(update.message.chat_id, text=message)


def remove_subscriber_handler(bot, update):
    message = SubscriptionHandler(update=update).unsubscribe()
    bot.sendMessage(update.message.chat_id, text=message)
