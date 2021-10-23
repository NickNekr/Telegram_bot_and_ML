import requests
import telebot

from ML import predict, get_data
from token_and_key import token, weather_key


def tg_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(message.chat.id,
                         "Hello, if you wanna current weather in something city - input city name!\nIf you wanna predict temp in moscow input date(year, month, day)!")

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if all(i.isdigit() for i in message.text.split()):
            try:
                inp_year, int_month, inp_day = map(int, message.text.split())
                get_data(inp_year, int_month, inp_day)
                bot.send_message(message.chat.id,
                                 f"Temp {':'.join(map(lambda x: x.zfill(2), message.text.split()[::-1]))} - " + str(
                                     round(predict(inp_year, int_month, inp_day)[0])) + ' Cel')
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Incorrect date')
        else:
            try:
                data = requests.get(
                    f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_key}&units=metric').json()
                city = data['name']
                temperature = data['main']['temp']
                wind_speed = data['wind']['speed']
                feels = data['main']['feels_like']
                bot.send_message(message.chat.id, f'Current weather in {city}:\n'
                                                  f'Temp - {temperature}\n'
                                                  f'Feels like {feels}\n'
                                                  f'Wind speed - {wind_speed}')
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, 'Incorrect city')

    bot.infinity_polling()


if __name__ == '__main__':
    tg_bot(token)
