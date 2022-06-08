import requests
import datetime
import asyncio
from config import meteo_token, bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from pprint import pprint

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    await message.reply('                     \U0001F32A Привет!!! \U0001F32A\n'
                        '\U0001F32A Напиши city+ и название города (city+магадан), я пришлю тебе погоду \U0001F32A'
                        )



@dp.message_handler()
async def get_weather(message: types.Message):
    if 'city+' in message.text.lower():
        a = message.text.lower()
        a = a.replace('city+', '')
        day = datetime.datetime.now()
        icon = {
            'Thunderstorm': '\U000026C8',
            'Drizzle': '\U0001F32B',
            'Rain': '\U0001F327',
            'Snow': '\U00002744',
            'Clear': '\U00002600',
            'Clouds': '\U000026C5'
        }
        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={a}&appid={meteo_token}&units=metric&lang=ru"
            )

            data = r.json()
            city_print = data['name']
            country_print = data['sys']['country']
            temperture_print = data['main']['temp']
            wind_print = data['wind']['speed']
            weather_print = str.capitalize(data['weather'][0]['description'])

            wind_deg_print = data['wind']['deg']
            if (337 <= wind_deg_print <= 360) or (0 <= wind_deg_print <= 22):
                wind_deg_print = 'Ветер: \U0001F32C северный'
            elif 23 <= wind_deg_print <= 67:
                wind_deg_print = 'Ветер: \U0001F32C северо-восточный'
            elif 68 <= wind_deg_print <= 112:
                wind_deg_print = 'Ветер: \U0001F32C восточный'
            elif 113 <= wind_deg_print <= 157:
                wind_deg_print = 'Ветер: \U0001F32C юго-восточный'
            elif 158 <= wind_deg_print <= 202:
                wind_deg_print = 'Ветер: \U0001F32C южный'
            elif 203 <= wind_deg_print <= 247:
                wind_deg_print = 'Ветер: \U0001F32C юго-западный'
            elif 248 <= wind_deg_print <= 292:
                wind_deg_print = 'Ветер: \U0001F32C западный'
            elif 293 <= wind_deg_print <= 336:
                wind_deg_print = 'Ветер: \U0001F32C северо-западный'

            weather_icon_print = data['weather'][0]['main']
            if weather_icon_print in icon:
                w_i_c = icon[weather_icon_print]
            else:
                w_i_c = '\U000026F1'

            await bot.send_message(message.from_user.id, f"Город: {city_print} ({country_print})"
                                 f"\n\U0001F4C5 {day.strftime('%d.%m.%Y')}"
                                 f"\n\U000023F0 {day.strftime('%H:%M')}"
                                 f"\n{weather_print} {w_i_c}"
                                 f"\nТемпература: \U0001F321 {temperture_print} С°\n{wind_deg_print} {wind_print} М/С"
                  )
            ans = await message.answer('Ответил в личку \U0001F60E')
            await message.delete()
            await asyncio.sleep(5)
            await ans.delete()

        except:
            ans1 = await message.reply('\U0001F625 Проверьте название города \U0001F625')
            await asyncio.sleep(5)
            await message.delete()
            await ans1.delete()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)