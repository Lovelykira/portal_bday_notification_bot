from abc import ABCMeta, abstractmethod
from datetime import timedelta, datetime


class Notification:
    __metaclass__ = ABCMeta

    def __init__(self, name, time, description):
        """
        Base class for notifications
        """
        self.name = name
        self.time = time
        self.description = description
        self.last_date_notify = datetime.now() - timedelta(days=1)

    @abstractmethod
    def generate_notification(self):
        """
        Should return notification message for user or None if no message should be shown
        """
        pass

    def get_name(self):
        return self.name

    def get_time(self):
        return self.time

    def get_description(self):
        return self.description
