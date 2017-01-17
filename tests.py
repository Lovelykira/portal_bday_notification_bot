import mock
import unittest

import msg
from server.handlers import SubscriptionHandler

from models import Subscriber, SubscriberNotification


class TestSubscriptionHandler(unittest.TestCase):

    def setUp(self):
        self.chat_id = -1

    def tearDown(self):
        try:
            sub = Subscriber.select().where(Subscriber.channel == -1)
            SubscriberNotification.delete().where(SubscriberNotification.subscriber == sub).execute()
            sub.delete_instance()
        except:
            pass

    @mock.patch('server.handlers.DBHandler')
    @mock.patch('server.handlers.NotificationService')
    def test_subscribe_one_new_one_unknown(self, notification_mock, db_mock):
        notification_mock.get_subscriptions.return_value = ['test_a', 'test_b']
        db_mock.return_value.get_user_subscriptions.return_value = []

        update = mock.Mock(message=mock.Mock(text='/subscribe test_a test_c', chat_id=self.chat_id))

        handler = SubscriptionHandler(update=update)
        message = handler.subscribe()

        db_mock.return_value.subscribe_user.assert_called_once_with('test_a')

        self.assertEqual(
            '{}{}'.format(
                msg.SUBSCRIPTION_INFO[msg.NEW_SUBSCRIPTION_KEY].format('test_a'),
                msg.SUBSCRIPTION_INFO[msg.UNKNOWN_SUBSCRIPTION_KEY].format('test_c')
            ),
            message
        )

    @mock.patch('server.handlers.DBHandler')
    @mock.patch('server.handlers.NotificationService')
    def test_subscribe_one_new_one_subscribed(self, notification_mock, db_mock):
        notification_mock.get_subscriptions.return_value = ['test_a', 'test_b']
        db_mock.return_value.get_user_subscriptions.return_value = ['test_b']

        update = mock.Mock(message=mock.Mock(text='/subscribe test_a test_b', chat_id=self.chat_id))

        handler = SubscriptionHandler(update=update)
        message = handler.subscribe()

        db_mock.return_value.subscribe_user.assert_called_once_with('test_a')

        self.assertEqual(
            '{}{}'.format(
                msg.SUBSCRIPTION_INFO[msg.ALREADY_SUBSCRIBED_KEY].format('test_b'),
                msg.SUBSCRIPTION_INFO[msg.NEW_SUBSCRIPTION_KEY].format('test_a')
            ),
            message
        )

    @mock.patch('server.handlers.DBHandler')
    @mock.patch('server.handlers.NotificationService')
    def test_subscribe_one_new_one_subscribed_one_unknown(self, notification_mock, db_mock):
        notification_mock.get_subscriptions.return_value = ['test_a', 'test_b']
        db_mock.return_value.get_user_subscriptions.return_value = ['test_b']

        update = mock.Mock(message=mock.Mock(text='/subscribe test_a test_b test_c', chat_id=self.chat_id))

        handler = SubscriptionHandler(update=update)
        message = handler.subscribe()

        db_mock.return_value.subscribe_user.assert_called_once_with('test_a')

        self.assertEqual(
            '{}{}{}'.format(
                msg.SUBSCRIPTION_INFO[msg.ALREADY_SUBSCRIBED_KEY].format('test_b'),
                msg.SUBSCRIPTION_INFO[msg.NEW_SUBSCRIPTION_KEY].format('test_a'),
                msg.SUBSCRIPTION_INFO[msg.UNKNOWN_SUBSCRIPTION_KEY].format('test_c')
            ),
            message
        )

    @mock.patch('server.handlers.DBHandler')
    @mock.patch('server.handlers.NotificationService')
    def test_subscribe_no_parameters(self, notification_mock, db_mock):
        notification_mock.get_subscriptions.return_value = ['test_a', 'test_b']
        notification_mock.get_notifications_description.return_value = {'test_a': 'descr_a',
                                                                        'test_b': 'descr_b'}
        db_mock.return_value.get_user_subscriptions.return_value = ['test_b']

        update = mock.Mock(message=mock.Mock(text='/subscribe', chat_id=self.chat_id))

        handler = SubscriptionHandler(update=update)
        message = handler.subscribe()

        db_mock.return_value.subscribe_user.assert_not_called()

        self.assertEqual(
             msg.AVAILABLE_SUBSCRIPTIONS.format('test_a - descr_a'),
            message
        )

    @mock.patch('server.handlers.DBHandler')
    @mock.patch('server.handlers.NotificationService')
    def test_unsubscribe_no_parameters(self, notification_mock, db_mock):
        notification_mock.get_subscriptions.return_value = ['test_a', 'test_b']
        notification_mock.get_notifications_description.return_value = {'test_a': 'descr_a',
                                                                        'test_b': 'descr_b'}
        db_mock.return_value.get_user_subscriptions.return_value = ['test_b']

        update = mock.Mock(message=mock.Mock(text='/unsubscribe', chat_id=self.chat_id))

        handler = SubscriptionHandler(update=update)
        message = handler.unsubscribe()

        db_mock.return_value.delete_subscription.assert_not_called()

        self.assertEqual(
             msg.AVAILABLE_UNSUBSCRIPTIONS.format('test_b - descr_b'),
            message
        )

    @mock.patch('server.handlers.DBHandler')
    @mock.patch('server.handlers.NotificationService')
    def test_unsubscribe_one_valid_one_unknown_one_not_subscribed(self, notification_mock, db_mock):
        notification_mock.get_subscriptions.return_value = ['test_a', 'test_b']
        notification_mock.get_notifications_description.return_value = {'test_a': 'descr_a',
                                                                        'test_b': 'descr_b'}
        db_mock.return_value.get_user_subscriptions.return_value = ['test_a']

        update = mock.Mock(message=mock.Mock(text='/unsubscribe test_a test_b test_c', chat_id=self.chat_id))

        handler = SubscriptionHandler(update=update)
        message = handler.unsubscribe()
        db_mock.return_value.delete_subscription.assert_called_with('test_a')

        self.assertEqual(
            '{}{}{}'.format(
            msg.SUBSCRIPTION_INFO[msg.UNSUBSCRIPTION_ERROR_KEY].format('test_b'),
            msg.SUBSCRIPTION_INFO[msg.UNSUBSCRIPTION_KEY].format('test_a'),
            msg.SUBSCRIPTION_INFO[msg.UNKNOWN_SUBSCRIPTION_KEY].format('test_c')
            ),
            message
        )




if __name__ == '__main__':
    unittest.main()
