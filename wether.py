from datetime import datetime
weather = {
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


def weather_cod(weather_code)->int:
    soat = datetime.now().hour+4
    if 0 <= soat < 3:
        weather_code = weather_code[0]
    elif 3 <= soat < 6:
        weather_code = weather_code[1]
    elif 6 <= soat < 9:
        weather_code = weather_code[2]
    elif 9 <= soat < 12:
        weather_code = weather_code[3]
    elif 12 <= soat < 15:
        weather_code = weather_code[4]
    elif 15 <= soat < 18:
        weather_code = weather_code[5]
    elif 18 <= soat < 21:
        weather_code = weather_code[6]
    else:
        weather_code=weather_code[6]
    return weather_code
