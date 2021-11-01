from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
import datetime
import json


def get_exchanges_keyboard(exchanges):
    keyboard = InlineKeyboardMarkup()

    for chunk in chunk_iterable(exchanges, 2):
        row_buttons = []
        for exchange in chunk:
            ccy_code = exchange['ccy']
            row_buttons.append(
                InlineKeyboardButton(
                    text=exchange['base_ccy'] + ' -> ' + ccy_code,
                    callback_data='{"a":"ex", "c":"' + ccy_code + '"}'
                )
            )
        keyboard.row(*row_buttons)

    return keyboard


def get_exchange_update_keyboard(exchange):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Update',
            callback_data=json.dumps({
                'a': 'u',
                'c': exchange['ccy'],
                'b': exchange['buy'],
                's': exchange['sale']
            })
        )
    )

    return keyboard


def get_exchange_text(currency_result, old_exchange_data=None):
    base_currency = currency_result['base_ccy']
    buy_now = currency_result['buy']
    sale_now = currency_result['sale']

    text = '<i>Currency exchange for ' + currency_result['ccy'] + ':</i>\n\n' + \
           '<b>Buy:</b> ' + buy_now + ' ' + base_currency + \
           (_get_diff(old_exchange_data['b'], buy_now) if old_exchange_data else '') + '\n' + \
           '<b>Sale:</b> ' + sale_now + ' ' + base_currency + \
           (_get_diff(old_exchange_data['s'], sale_now) if old_exchange_data else '')

    # if update action - add signature with datetime
    if old_exchange_data:
        text += '\n\n<i>Updated ' + datetime.datetime.now().strftime('%H:%M:%S %Y-%m-%d') + '</i>'

    return text


def _get_diff(before, now):
    diff = float('%.6f' % (float(before) - float(now)))
    if diff > 0:
        return ' (' + str(diff) + ' ↗)'
    elif diff < 0:
        return ' (' + str(abs(diff)) + ' ↘)'
    return ''


def chunk_iterable(iterable, chunk_size):
    return [iterable[i:i + chunk_size] for i in range(0, len(iterable), chunk_size)]
