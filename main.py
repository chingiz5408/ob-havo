from datetime import datetime
import asyncio
import logging
import sys
import os
import  requests
from aiogram import Bot, Dispatcher, html,types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command,CommandObject
from aiogram.types import Message,KeyboardButton,ReplyKeyboardMarkup,InputFile,FSInputFile

import local_token as lt
import pymysql
keyboard=ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Bugungi ob havo"),KeyboardButton(text="ertangi ob havo")],
    [KeyboardButton(text="haftalik ob Havo"),KeyboardButton(text="10 kunlik")]
], resize_keyboard=True)


bot = Bot(token=lt.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
db=pymysql.connect(
    host="localhost",
    user="chingiz",
    password="azar5408",
    database="chingiz_dev",
)
cursor=db.cursor()
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
weather_descriptions = {
                    0: ("Quyoshli", "Quyoshli.jpg"),
                    1: ("Qisman bulutli", "Qisman_bulutli.jpg"),
                    2: ("O'rtacha bulutli", "O'rtacha_bulutli.jpg"),
                    3: ("Qalin bulutli", "Qalin_bulutli.jpg"),
                    45: ("Tuman", "Tuman.jpg"),
                    48: ("Tuman (sovuq yomg'irli)", "Tuman_(sovuq_yomg'irli).jpg"),
                    51: ("Yengil yomg'ir", "Yengil_yomg'ir.jpg"),
                    53: ("Kuchsiz yomg'ir", "Kuchsiz_yomg'ir.jpg"),
                    55: ("Kuchli yomg'ir", "Kuchli_yomg'ir.jpg"),
                    56: ("Yengil muzli yomg'ir", "Yengil_muzli_yomg'ir.jpg"),
                    57: ("Muzli yomg'ir", "Muzli_yomg'ir.jpg"),
                    61: ("Yengil yomg'ir", "Yengil_yomg'ir.jpg"),
                    63: ("Kuchsiz yomg'ir", "Kuchsiz_yomg'ir.jpg"),
                    65: ("Kuchli yomg'ir", "Kuchli_yomg'ir.jpg"),
                    66: ("Yengil muzli yomg'ir", "Yengil_muzli_yomg'ir.jpg"),
                    67: ("Muzli yomg'ir", "Muzli_yomg'ir.jpg"),
                    71: ("Yengil qor", "Yengil_qor.jpg"),
                    73: ("Qor", "Qor.jpg"),
                    75: ("Kuchli qor", "Kuchli_qor.jpg"),
                    77: ("Qor donalari", "Qor_donalari.jpg"),
                    85: ("Yengil qorli yomg'ir", "Yengil_qorli_yomg'ir.jpg"),
                    86: ("Qorli yomg'ir", "Qorli_yomg'ir.jpg"),
                    80: ("Yengil yomg'ir", "Yengil_yomg'ir.jpg"),
                    81: ("Kuchsiz yomg'ir", "Kuchsiz_yomg'ir.jpg"),
                    82: ("Kuchli yomg'ir", "Kuchli_yomg'ir.jpg"),
                    95: ("Kuchsiz momaqaldiroq", "Kuchsiz_momaqaldiroq.jpg"),
                    96: ("Kuchli momaqaldiroq", "Kuchli_momaqaldiroq.jpg"),
                    99: ("Juda kuchli momaqaldiroq", "Juda_kuchli_momaqaldiroq.jpg"),
                }
@dp.message()
async def echo_handler(message: Message) -> None:
    global time_last,last_response,weather_code,weather_descriptions
    if message.text=="Bugungi ob havo":
        now=datetime.today().hour
        url = (
            "https://api.open-meteo.com/v1/forecast?latitude=39.6542&longitude=66.9695"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max,weathercode"
            "&timezone=auto"
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            max_temp = data['daily']['temperature_2m_max'][0]
            min_temp = data['daily']['temperature_2m_min'][0]
            precipitation = data['daily']['precipitation_sum'][0]
            max_wind_speed = data['daily']['windspeed_10m_max'][0]
            weather_code = data['daily']['weathercode'][0]

            discription, rasm = weather_descriptions.get(weather_code, ("Ob-havo holati noma'lum", "unknown.png"))
            time_last = now
            last_response=(
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

            rasm_file = "./galireya/"+rasm
            # if not os.path.exists(rasm_file):
            #     await message.answer("Kiritilgan fayl yo'q yoki noto'g'ri manzil ko'rsatilgan!")
            # else :
            #     await message.answer("Kiritilgan fayl bor yoki yaxshi manzil ko'rsatilgan!")
            try:
                photo = FSInputFile(rasm_file)
                await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=last_response)
                  # Rasmni InputFile sifatida o'zgartirish
                # await message.answer_photo(photo, caption="Mana sizning rasmingiz!")
            except Exception as e:
                await message.answer(f"Xatolik yuz berdi: {e}")
        else:
            await message.answer("Ob-havo ma'lumotlarini olishda xatolik yuz berdi!")
        # if time_last is None or now != time_last:
        #     print("salom")
        # else:
        #     await message.answer(f"Bugun soat-{time_last} da\n {last_response}")

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
