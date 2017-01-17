from server.server import BotServer

def check_database():
    """
    Create tables if doesn't exists
    """
    from models import Subscriber, SubscriberNotification
    check_exist(Subscriber)
    check_exist(SubscriberNotification)


def check_exist(model):
    try:
        model.select().count()
    except Exception:
        from models import db
        db.connect()
        db.create_tables([model])


if __name__ == '__main__':
    check_database()
    BotServer().run()
