import numbers
from datetime import timedelta, datetime
import itertools
from collections import namedtuple
import unittest

Confirmation = namedtuple('Confirmation', 'account_number transaction_code transaction_id time_utc time')


class TimeZone:
    def __init__(self, name, offset_hours, offset_minutes):
        if name is None or len(str(name).strip()) == 0:
            raise ValueError('Timezone name cannot be empty.')
        self._name = str(name).strip()

        if not isinstance(offset_hours, numbers.Integral):
            raise ValueError('Hour offset must be an integer')

        if not isinstance(offset_minutes, numbers.Integral):
            raise ValueError('Minute offset must be an integer')

        if offset_minutes > 59 or offset_minutes < -59:
            raise ValueError('Minutes offset must be between -59 and 59.')

        offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0):
            raise ValueError('Offset must be between -12:00 and +14:00')

        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset

    @property
    def offset(self):
        return self._offset

    @property
    def name(self):
        return self._name

    def __eq__(self, other):
        return (isinstance(other, TimeZone) and
                self.name == other.name and
                self._offset_hours == other._offset_hours and
                self._offset_minutes == other._offset_minutes)

    def __repr__(self):
        return (f"TimeZone(name='{self.name}', "
                f"offset_hours={self._offset_hours}, "
                f"offset_minutes={self._offset_minutes})")


# tz1=TimeZone('Helsinki',-2,-15)
# dt=datetime.utcnow()
# print(dt)
# print(dt+tz1.offset)


class Account:
    transaction_counter = itertools.count(100)
    _interest_rate = 0.5  # private variable

    _transaction_codes = {
        'deposit': 'D',
        'withdraw': 'W',
        'interest': 'I',
        'rejected': 'X'
    }

    def __init__(self, account_number, first_name, last_name,
                 timezone=None, initial_balance=0):
        self._account_number = account_number
        self.first_name = first_name
        self.last_name = last_name

        if timezone is None:
            timezone = TimeZone('UTC', 0, 0)
        self.timezone = timezone

        self._balance = Account.validate_real_number(initial_balance, min_value=0)

    @property  # read-only property
    def account_number(self):
        return self._account_number

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        self.validate_and_set_name('_first_name', value, 'First name')

    @property
    def last_name(self):
        return self._last_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def balance(self):
        return self._balance

    @property  # this is instance property
    def timezone(self):
        return self._timezone

    @timezone.setter
    def timezone(self, value):
        if not isinstance(value, TimeZone):
            raise ValueError('Please insert a valid time zone')
        self._timezone = value

    @classmethod  # we apply class method to get and set interest rate
    # at class level
    def get_interest_rate(cls):
        return cls._interest_rate

    @classmethod
    def set_interest_rate(cls, value):
        if not isinstance(value, numbers.Real):
            raise ValueError('Interest rate must be a real number.')
        if value < 0:
            raise ValueError('Interest rate cannot be negative')
        cls._interest_rate = value

    def generate_confirmation_code(self, transaction_code):
        dt_str = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        return f'{transaction_code}-{self.account_number}-{dt_str}-{next(Account.transaction_counter)}'

    @last_name.setter
    def last_name(self, value):
        self.validate_and_set_name('_last_name', value, 'Last name')

    def validate_and_set_name(self, attr_name, value, field_title):
        if value is None or len(str(value).strip()) == 0:
            raise ValueError(f'{field_title} cannot be empty')
        setattr(self, attr_name, value)

    @staticmethod
    def validate_real_number(value, min_value=None):
        if not isinstance(value, numbers.Real):
            raise ValueError('Value must be a real number')

        if min_value is not None and value < min_value:
            raise ValueError(f'Value must be at least {min_value}')

        return value

    @staticmethod
    def parse_confirmation_code(confirmation_code, preferred_time_zone=None):
        # dummy-A100-20200603145530-101
        parts = confirmation_code.split('-')
        if len(parts) != 4:
            raise ValueError('Invalid confirmation code')

        transaction_code, account_number, raw_dt_utc, transaction_id = parts
        # unpacking parts into 4 parts

        try:
            dt_utc = datetime.strptime(raw_dt_utc, '%Y%m%d%H%M%S')
        except ValueError as ex:
            raise ValueError('Invalid transaction datetime.') from ex

        if preferred_time_zone is None:
            preferred_time_zone = TimeZone('UTC', 0, 0)

        if not isinstance(preferred_time_zone, TimeZone):
            raise ValueError('Invalid Timezone')

        dt_preferred = dt_utc + preferred_time_zone.offset
        dt_preferred_str = f"{dt_preferred.strftime('%Y-%m-%d %H:%M:%S')} ({preferred_time_zone.name})"
        return Confirmation(account_number, transaction_code,
                            transaction_id, dt_utc.isoformat(), dt_preferred_str)

    def deposit(self, value):
        value = Account.validate_real_number(value, 0.01)
        transaction_code = Account._transaction_codes['deposit']
        conf_code = self.generate_confirmation_code(transaction_code)
        self._balance += value
        return conf_code

    def withdraw(self, value):
        value = Account.validate_real_number(value, 0.01)
        accepted = False
        if self.balance - value < 0:
            transaction_code = Account._transaction_codes['rejected']
        else:
            accepted = True
            transaction_code = Account._transaction_codes['withdraw']

        conf_code = self.generate_confirmation_code(transaction_code)

        if accepted:
            self._balance -= value

        return conf_code

    def pay_interest(self):
        interest = self.balance * Account.get_interest_rate() / 100
        conf_code = self.generate_confirmation_code(self._transaction_codes['interest'])
        self._balance += value
        return conf_code


# a=Account('A100','Nabi','Rahimov')
# con_code=a.generate_confirmation_code(Account._transaction_codes['deposit'])
# ac=Account.parse_confirmation_code(con_code,preferred_time_zone=TimeZone('ABC',-1,0))
# print(ac)

# a=Account('A100','Nabi','Rahimov',initial_balance=100)
# print(a.balance)

# try:
#     a.deposit(-150)
# except ValueError as ex:
#     print(ex)

# print(a.deposit(5000))
# print(a.balance)
# print(a.withdraw(2000))
# print(a.balance)


# Unittest
def run_tests(test_class):
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


class TestAccount(unittest.TestCase):

    def test_create_timezone(self):
        tz = TimeZone('ABC', -1, -30)
        self.assertEqual('ABC', tz.name)
        self.assertEqual(timedelta(hours=-1, minutes=-30), tz.offset)

    def test_timezones_equal(self):
        tz1 = TimeZone('ABC', -1, -30)
        tz2 = TimeZone('ABC', -1, -30)
        self.assertEqual(tz1, tz2)

    def test_timezones_not_equal(self):
        tz = TimeZone('ABC', -1, -30)

        test_timezones = (
            TimeZone('Helsinki', -1, -30),
            TimeZone('ABC', -1, 0),
            TimeZone('ABC', 1, -30)
        )

        for i, test_tz in enumerate(test_timezones):
            with self.subTest(test_name=f'Test # {i}'):
                self.assertNotEqual(tz, test_tz)


run_tests(TestAccount)
