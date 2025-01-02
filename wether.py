from datetime import datetime
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
