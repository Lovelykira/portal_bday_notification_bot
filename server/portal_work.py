import requests
import json

from datetime import date

import conf
import msg


class CanNotAutorize(Exception):
    message = msg.AUTHENTICATE_ERROR


class Birthdays:

    def get_weekly_birthdays(self):
        token = self._authenticate()
        try:
            return json.loads(self._request_birthdays(token).text)
        except Exception:
            return []

    def get_todays_birthdays(self):
        birthday_people = self.get_weekly_birthdays()
        try:
            for man in birthday_people:
                if not self.birthday_is_today(man['birth_date']):
                        birthday_people.remove(man)
            return birthday_people
        except Exception:
            return []

    def birthday_is_today(self, mans_birthday):
        return mans_birthday[4:] == date.today().isoformat()[4:]

    def _request_birthdays(self, token):
        return requests.get(conf.LIGHT_IT_API_URL_DEV + conf.BIRTHDAY_API_URL, headers=self._get_header(token))

    def _authenticate(self):
        results = requests.post(conf.LIGHT_IT_API_URL_DEV + conf.LOGIN_API_URL, data=self._get_login_data())
        authenticate_data = json.loads(results.text)
        self._validate(authenticate_data)
        return authenticate_data['key']

    @classmethod
    def _validate(cls, authenticate_data):
        if 'key' not in authenticate_data:
            raise CanNotAutorize()

    @classmethod
    def _get_login_data(cls):
        return {'email': conf.username_dev, 'password': conf.password_dev}

    @classmethod
    def _get_header(cls, token):
        return {'User-Agent': conf.USER_AGENT, 'Authorization': 'Token %s' % token}
