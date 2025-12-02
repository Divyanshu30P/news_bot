import os
import requests
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌤️ Hello! I am your Weather Bot.\n"
        "Send /weather <city name> to get the current weather."
    )

@bot.message_handler(commands=["weather"])
def get_weather(message):
    city = message.text.replace("/weather", "").strip()
    if not city:
        bot.send_message(message.chat.id, "Please provide a city name after /weather")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("cod") != 200:
            bot.send_message(message.chat.id, f"City not found: {city}")
            return

        name = response["name"]
        country = response["sys"]["country"]
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]

        weather_report = (
            f"🌍 Weather in {name}, {country}:\n"
            f"Temperature: {temp}°C\n"
            f"Condition: {desc}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        bot.send_message(message.chat.id, weather_report)

    except Exception as e:
        bot.send_message(message.chat.id, f"Error fetching weather: {e}")

bot.polling()
