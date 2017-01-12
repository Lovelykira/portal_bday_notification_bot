import requests
import json

from datetime import date

import conf


def birthday_is_today(mans_birthday):
    return mans_birthday[4:] == date.today().isoformat()[4:]


def get_weekly_birthdays():
    res = requests.post( conf.LIGHT_IT_URL + '/api/auth/login/', data={'email': conf.username,
                                                                       'password': conf.password})
    try:
        token = json.loads(res.text)['key']
        res = requests.get( conf.LIGHT_IT_URL + '/api/week_birthdays/',
                           headers={
                               'User-Agent': conf.USER_AGENT,
                               'Authorization': 'Token ' + token
                                }
                           )
        birthday_people = json.loads(res.text)
        return birthday_people
    except:
        return []


def get_todays_birthdays():
    birthday_people = get_weekly_birthdays()
    try:
        for man in birthday_people:
            if not birthday_is_today(man['birth_date']):
                birthday_people.remove(man)
        return birthday_people
    except:
        return []