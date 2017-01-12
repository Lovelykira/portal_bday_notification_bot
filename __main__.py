from server.server import BotServer

def check_database():
    """
    Create tables if doesn't exists
    """
    from models import Subscriber
    try:
        Subscriber.select().count()
    except Exception:
        from models import db
        db.connect()
        db.create_tables([Subscriber])


if __name__ == '__main__':
    check_database()
    BotServer().run()
