from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback
import telebot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Формат запроса валют <валюта которую надо конвертировать> <валюта на которую надо конвертировать> " \
           "<количество валюты>  \n команда /values покажет доступные валюты для конвертации "
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values_message = message.text.split(' ')
    try:
        if len(values_message) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convertor.get_price(*values_message)
    except APIException as error:
        bot.reply_to(message, f"Ошибка в команде:\n{error}")
    except Exception as error:
        traceback.print_tb(error.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{error}")
    else:
        bot.reply_to(message, answer)


bot.polling()
