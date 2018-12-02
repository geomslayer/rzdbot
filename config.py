# coding: utf-8

from collections import namedtuple

TOKEN = 'put token here'

Train = namedtuple('Train', 'url desc id seat_types')

# in urls must be {date} pattern
TRAINS = [
    Train(
        url='https://pass.rzd.ru/tickets/public/ru?layer_name=e3-route&st0=МОСКВА&code0=2000000&dt0={date}&st1=ТОЛЬЯТТИ&code1=2024810&checkSeats=1',
        desc='Moscow-Togliatti',
        id='066й',
        seat_types=frozenset(['плацкартный'])
    ),
]

MY_CHAT_ID = 162913520

DESIRED_DATES = ['28.12.2018', '29.12.2018', '30.12.2018']

# delay between tickets check (second)
CHECKING_DELAY = 300
