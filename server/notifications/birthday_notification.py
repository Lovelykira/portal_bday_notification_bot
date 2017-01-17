import msg
import datetime

from server.portal_work import Birthdays
from server.notification_service import NotificationService

from .notification import Notification


class BirthdayNotification(Notification):
    """
    Class to notificate about today's birthdays
    """

    def generate_notification(self):
        """
        Returns:
            message that contains first name and last name of today's birthday people
            error-message if error occurred
            None if no birthdays today
        """
        try:
            birthdays_people = self.get_birthday_people()
            if not birthdays_people:
                return None
                # return msg.NO_BIRTHDAYS
            birthdays = ', '.join(['{} {}'.format(man['first_name'], man['last_name']) for man in birthdays_people])
            return msg.BIRTHDAY_NOTIFICATION.format(birthdays)
        except:
            return msg.BIRTHDAYS_PARSE_ERROR

    def get_birthday_people(self):
        birthdays = Birthdays().get_todays_birthdays()
        return birthdays

NotificationService().register(BirthdayNotification(name='birthday', time='11:21', description='Уведомления о днях рождения'))