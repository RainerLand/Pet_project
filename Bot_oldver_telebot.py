import telebot
import json
import requests
from telebot import types
API = '7eed521909ce08b77ca1b16c66e318b9'
bot = telebot.TeleBot('6505027295:AAEcEELvKEbj_vjjCKu_pwGUZsIIrcjOu1s')


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>, я могу подсказать тебе погоду в твоем городе. Введи название!'
    bot.send_message(message.chat.id, mess , parse_mode='html')
    
#  любой текстовый запрос
@bot.message_handler(content_types=['text'])
def weather(message):
    # п город из сообщения пользователя
  city = message.text
  # запрос
  url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
  # отправляем запрос на сервер и сразу получаем результат
  weather_data = requests.get(url).json()
  print(weather_data)
  # получаем данные о температуре и о том, как она ощущается
  temperature = round(weather_data['main']['temp'])
  temperature_feels = round(weather_data['main']['feels_like'])
  #  ответы
  w_now = 'Сейчас в городе ' + city + ' ' + str(temperature) + ' °C'
  w_feels = 'Ощущается как ' + str(temperature_feels) + ' °C'
  # отправляем значения пользователю
  bot.send_message(message.from_user.id, w_now)
  bot.send_message(message.from_user.id, w_feels)
  #  ветреная погоду
  wind_speed = round(weather_data['wind']['speed'])
  if wind_speed < 5:
      bot.send_message(message.from_user.id, '✅ Погода хорошая, ветра почти нет')
  elif wind_speed < 10:
      bot.send_message(message.from_user.id, '🤔 На улице ветрено, оденьтесь чуть теплее')
  elif wind_speed < 20:
      bot.send_message(message.from_user.id, '❗️ Ветер очень сильный, будьте осторожны, выходя из дома')
  else:
      bot.send_message(message.from_user.id, '❌ На улице шторм, на улицу лучше не выходить')  

# запуск бота
if __name__ == '__main__':
    while True:
        # цикл опроса новых сообщений
        try:
            bot.polling(none_stop=True, interval=0)
        # если возникла ошибка , без остановки работы
        except Exception as e: 
            print('❌❌❌❌❌ Сработало исключение! ❌❌❌❌❌')












