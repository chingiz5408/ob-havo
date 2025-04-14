import asyncio
import logging
import sys
import requests
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram.types import Message,KeyboardButton,ReplyKeyboardMarkup,FSInputFile
import local_token as lt
from datetime import datetime
from db import get_db_connection
from Joylashuvlar import joylar

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Toshkent sh"), KeyboardButton(text="Toshkent vil.")],
        [KeyboardButton(text="Andijon"), KeyboardButton(text="Buxoro")],
        [KeyboardButton(text="Farg‘ona"), KeyboardButton(text="Jizzax")],
        [KeyboardButton(text="Xorazm"), KeyboardButton(text="Namangan")],
        [KeyboardButton(text="Navoiy"), KeyboardButton(text="Qashqadaryo")],
        [KeyboardButton(text="Qoraqalpog‘iston"), KeyboardButton(text="Samarqand")],
        [KeyboardButton(text="Sirdaryo"), KeyboardButton(text="Surxondaryo")],
        [KeyboardButton(text="Haftalik")],
    ],
    resize_keyboard=True
)


bot = Bot(token=lt.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO men(name, familiya, course) VALUES (%s, %s, %s)",
            (
                message.from_user.full_name or "Unknown",
                message.from_user.username or "Unknown",
                "some_course"
            )
        )
        db.commit()
        cursor.close()
        db.close()
        await message.answer(
            f"Salom, {html.bold(message.from_user.full_name or 'User')}!",
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"Error: {e}")
        await message.answer("sizni bazaga qo'sha olmadik")

@dp.message(Command(commands=['user']))
async def users(message: Message):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM men")
        result = cursor.fetchall()
        print(result)
        cursor.close()
        if result:
            for row in result:
                text = f"Id=>{row[0]}\n Fullname=>{row[1]}\n Username=>{row[2]}\n Kursi=>{row[3]}"
                await message.answer(text=text, reply_markup=keyboard)
        else:
            await message.answer("foydalanuvchi topilmadi.")
    except Exception as e:
        print(f"Error: {e}")
        await message.answer(f"xato {e}")
    finally:
        db.close()



time_last = None
last_response = None
weather_code=-1

def getInfo(manzil):
    if manzil in joylar:
        kenglik = joylar[manzil][0]
        uzunlik = joylar[manzil][1]
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={kenglik}&longitude={uzunlik}"
            "&hourly=temperature_2m,precipitation,weathercode,windspeed_10m"
            "&timezone=auto"
        )
        response = requests.get(url)
        return response
    else:
        return "Bunday manzil mavjud emas"


def makeMessage(discription, temperature, precipitation, wind_speed, holat, jarayon, tavsiya) -> str:
    response = (
        f"{holat} Ayni paytdagi Ob-havo\n"
        "━━━━━━━━━━━━━━━ \n"
        f"📆 {datetime.now().strftime('Sana: %d-%m-%Y  Vaqt: %H:%M')}\n"
        f"🕒 Holat: {discription} {jarayon}\n"
        f"🌡 Harorat: {temperature}°C\n"
        f"💧 Yog'ingarchilik: {precipitation} mm\n"
        f"🌬 Shamol tezligi: {wind_speed} km/soat\n"
        "━━━━━━━━━━━━━━━\n"
        f"{tavsiya}\n"
        f"❓ Bugungi rejalaringiz qanday?"
    )
    return response


def getWeatherStatus(code):
    db = get_db_connection()
    cursor=db.cursor()
    cursor.execute(f"SELECT * FROM `weather` WHERE code={code}")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

@dp.message()
async def echo_handler(message: Message) -> None:
    global time_last, last_response, weather_code
    if message.text:
        response = getInfo(message.text)
        if isinstance(response, str):
            await message.answer(response)
        else:
            if response.status_code == 200:
                data = response.json()

                now = datetime.now().strftime('%Y-%m-%dT%H:00')
                times = data['hourly']['time']
                
                if now in times:
                    index = times.index(now)
                else:
                    index = 0  # fallback

                temperature = data['hourly']['temperature_2m'][index]
                precipitation = data['hourly']['precipitation'][index]
                wind_speed = data['hourly']['windspeed_10m'][index]
                weather_code_val = data['hourly']['weathercode'][index]

                result = getWeatherStatus(weather_code_val)
                if result:
                    discription = result[0][2]
                    rasm = result[0][3]
                    holat = result[0][4]
                    jarayon = result[0][5]
                    tavsiya = result[0][6]

                    last_response = makeMessage(discription, temperature, precipitation, wind_speed, holat, jarayon, tavsiya)
                    rasm_file = "./galireya/" + rasm

                    try:
                        photo = FSInputFile(rasm_file)
                        await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=last_response)
                    except Exception as e:
                        await message.answer(f"Xatolik yuz berdi: {e}")
                else:
                    await message.answer("Ma'lumotlar bazasidan ob-havo kodi topilmadi.")
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
