DATABASE_NAME = 'subscribers_db'
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
BOT_TOKEN = '307624948:AAFKyfSHRabT-lhqIIeWFXUM6gh5UwsW36E'
LIGHT_IT_URL = 'https://www.portal.light-it.net'
# LIGHT_IT_URL_DEV = 'https://www.infoportal-dev.tk'

try:
    from local import *
except ImportError:
    pass
