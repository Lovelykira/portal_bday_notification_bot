DATABASE_NAME = 'subscribers_db'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

LIGHT_IT_API_URL = 'https://www.portal.light-it.net'
LIGHT_IT_API_URL_DEV = 'https://www.infoportal-dev.tk'

LOGIN_API_URL = '/api/auth/login/'
BIRTHDAY_API_URL = '/api/week_birthdays/'

try:
    from local import *
except ImportError:
    pass
