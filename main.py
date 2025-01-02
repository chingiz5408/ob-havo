import asyncio
import logging
import sys
import  requests
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,KeyboardButton,ReplyKeyboardMarkup,FSInputFile
import local_token as lt
from datetime import datetime
from .db import *
from .Joylashuvlar import joylar
from .wether import weather,weather_cod

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Toshkent sh"), KeyboardButton(text="Toshkent vil.")],
        [KeyboardButton(text="Andijon"), KeyboardButton(text="Buxoro")],
        [KeyboardButton(text="Farg‘ona"), KeyboardButton(text="Jizzax")],
        [KeyboardButton(text="Xorazm"), KeyboardButton(text="Namangan")],
        [KeyboardButton(text="Navoiy"), KeyboardButton(text="Qashqadaryo")],
        [KeyboardButton(text="Qoraqalpog‘iston"), KeyboardButton(text="Samarqand")],
        [KeyboardButton(text="Sirdaryo"), KeyboardButton(text="Surxondaryo")],
        [KeyboardButton(text="10 kunlik")],
    ],
    resize_keyboard=True
)


bot = Bot(token=lt.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    cursor.execute("INSERT INTO men(name,familiya,course) VALUES(%s,%s,%s)",
    (message.from_user.full_name, message.from_user.first_name, "some_course"))
    db.commit()
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@dp.message(Command(commands=['user']))
async def users(message: Message):
    cursor.execute("SELECT * FROM men")
    result=cursor.fetchall()
    for i in result:
        text=f"{i[0]}-{i[1]}-{i[2]}-{i[3]}"
        await message.answer(text=text,reply_markup=keyboard)

time_last = None
last_response = None
weather_code=-1

def getInfo(manzil):
    kenglik=joylar[manzil][0]
    uzunlik=joylar[manzil][1]
    url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={kenglik}&longitude={uzunlik}"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,weathercode"
            "&timezone=auto"
    )
    response = requests.get(url)
    return response

def makeMessage(discription,max_temp,min_temp,precipitation,max_wind_speed)->str:
    last_response = (
        f"🌨 Bugungi Ob-havo Ma'lumotlari\n"
        "━━━━━━━━━━━━━━━ \n"
        f"📆 {datetime.now().strftime('Sana: %d-%m-%Y  Vaqt: %H:%M')}\n"
        f"🕒 Holat: {discription} yog'moqda!\n"
        f"❄ Haroratlar:{max_temp}°C\n"
        f"▫ Maksimal: {max_temp}°C 🌡\n"
        f"▫ Tunda: {min_temp}°C 🥶\n"
        f"💧 Yog'ingarchilik miqdori: {precipitation} mm\n"
        f"🌬 Shamol tezligi: {max_wind_speed} km/soat 🌪\n"
        "━━━━━━━━━━━━━━━\n"
        f"⚠️ Iltimos, ehtiyot bo'ling: qor yo'llarni sirpanchiq qilishi mumkin!\n"
        f"❓ Bugungi rejalaringiz qanday? ❄"
    )
    return last_response

@dp.message()
async def echo_handler(message: Message) -> None:
    global time_last,last_response,weather_code
    if message.text:
        response = getInfo(message.text)
        if response.status_code == 200:
            data = response.json()
            max_temp = data['daily']['temperature_2m_max'][0]
            min_temp = data['daily']['temperature_2m_min'][0]
            precipitation = data['daily']['precipitation_sum'][0]
            max_wind_speed = data['daily']['windspeed_10m_max'][0]
            weather_code = data['daily']['weathercode']
            weather_code=weather_cod(weather_code)
            discription, rasm = weather.get(weather_code, ("Ob-havo holati noma'lum", "unknown.png"))
            last_response=makeMessage(discription,max_temp,min_temp,precipitation,max_wind_speed)
            rasm_file = "./galireya/"+rasm
            try:
                photo = FSInputFile(rasm_file)
                await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=last_response)
            except Exception as e:
                await message.answer(f"Xatolik yuz berdi: {e}")
        else:
            await message.answer("Ob-havo ma'lumotlarini olishda xatolik yuz berdi!")

async def main() -> None:
    global  bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("bot.log"),#bu qism holatni bot.log filega yozib bpradi
            logging.StreamHandler(sys.stdout)#bu qism terminalda holatni bildirib turadi
        ]
                        )
    asyncio.run(main())
