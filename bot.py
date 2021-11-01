import config, utils
import json
from telebot import TeleBot
from pb_service import PBService

# init bot by token from config
bot = TeleBot('1740123275:AAHJ6m-ytiNxQwfthKq328dTW59vv47u9-4')
pb_service = PBService()


# handle /start
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Welcome! I\' m glad to see you!'
    )


# handle /help
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Ok. Here is help to you:\n\n' +
             '/exchange - show currencies list. Then click on currency code to see exchange.'
    )


# handle /exchange
@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    bot.send_message(
        chat_id=message.chat.id,
        text='Here are available exchanges. Select one of them:',
        reply_markup=utils.get_exchanges_keyboard(pb_service.get_exchanges())
    )


# handle all callback queries with "exchanges" action
@bot.callback_query_handler(func=lambda query: json.loads(query.data)['a'] == 'ex')
def choose_exchange_callback(query):
    # get chosen currency from callback query (ex-<currency>)
    chosen_currency = json.loads(query.data)['c']

    chat_id = query.message.chat.id

    # disables 'loading' state and adds 'typing' title to chat
    bot.answer_callback_query(query.id)
    bot.send_chat_action(chat_id, 'typing')

    # get data from pb_service by chosen currency
    currency_result = pb_service.get_exchange_by_currency(chosen_currency)

    bot.send_message(
        chat_id=chat_id,
        text=utils.get_exchange_text(currency_result),
        parse_mode='HTML',
        reply_markup=utils.get_exchange_update_keyboard(currency_result)
    )


# handle all callback queries with "update" action
@bot.callback_query_handler(func=lambda query: json.loads(query.data)['a'] == 'u')
def update_exchange_callback(query):

    # disables 'loading' state
    bot.answer_callback_query(query.id)

    # get currency from callback data and fetch actual information
    callback_data = json.loads(query.data)
    currency = callback_data['c']
    updated_data = pb_service.get_exchange_by_currency(currency)

    # edit old message
    bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=utils.get_exchange_text(updated_data, old_exchange_data=callback_data),
        parse_mode='HTML',
        reply_markup=utils.get_exchange_update_keyboard(updated_data)
    )


# use long poll non-stop
bot.polling(none_stop=True)
