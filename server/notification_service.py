import datetime

from models import SubscriberNotification


class NotificationService:
    """
    Handles all notifications
    """
    NOTIFICATIONS = {}

    def call_current_time_notifications(self, bot):
        """
        For every notification that wasn't sent today calls generate_notification().
        If it returns a message sends it to all subscribers.
        Args:
            bot: Bot instance to send a message
        """
        for name, notification_service in self.get_current_time_notifications().items():
            if self._notified_today(notification_service):
                continue
            self._update_notification_day(notification_service)

            for sub in SubscriberNotification.select().where(SubscriberNotification.notification_name == name):
                message = notification_service.generate_notification()
                if message:
                    bot.sendMessage(sub.subscriber.channel, message)

    def _notified_today(self, notification_service):
        """
        Checks if notification was sent today.
        Returns: True if it was sent. False otherwise.
        """
        return notification_service.last_date_notify.date() >= datetime.datetime.now().date()

    def _update_notification_day(self, notification_service):
        notification_service.last_date_notify = datetime.datetime.now()

    def get_current_time_notifications(self):
        """
        Finds all notifications that should be sent at the moment.
        Returns: notifications
        """
        now = datetime.datetime.now().time()
        notifications = {}
        for name in self.NOTIFICATIONS.keys():
            if self.NOTIFICATIONS[name].get_time() == self._format_time(now):
                notifications[name] = self.NOTIFICATIONS[name]
        return notifications

    def _format_time(self, time):
        return str(time)[:5]

    @classmethod
    def register(cls, service):
        cls.NOTIFICATIONS[service.name] = service

    @classmethod
    def get_subscriptions(cls):
        return cls.NOTIFICATIONS.keys()

    @classmethod
    def get_notifications_description(cls, notification_keys):
        result = {}
        if notification_keys == 'all':
            notification_keys = cls.NOTIFICATIONS.keys()
        for key in notification_keys:
            if key in cls.NOTIFICATIONS.keys():
                result[key] = cls.NOTIFICATIONS[key].get_description()
        return result
