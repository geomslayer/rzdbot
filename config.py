from collections import namedtuple

TOKEN = 'put token here'

Train = namedtuple('Train', 'url desc')

# in urls must be {date} pattern
TRAINS = [
    Train(
        url='https://pass.rzd.ru/tickets/public/ru?layer_name=e3-route&st0=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&code0=2000000&st1=%D0%A2%D0%BE%D0%BB%D1%8C%D1%8F%D1%82%D1%82%D0%B8&code1=2024810&dt0={date}&tfl=3&checkSeats=1',
        desc='Moscow-Togliatti',
    )
]

MY_CHAT_ID = 162913520

DESIRED_DATES = ['29.12.2017', '30.12.2017']

# delay between tickets check (second)
CHECKING_DELAY = 60
