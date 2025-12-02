import requests
from bs4 import BeautifulSoup
import telebot
import os

# Telegram Bot token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Function to scrape website
def get_headlines():
    url = "https://www.bbc.com/news"  # Example site
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    headlines = []

    # Example: get headlines in <h3> tags (modify for your target site)
    for h3 in soup.find_all("h3"):
        text = h3.get_text(strip=True)
        if text and text not in headlines:
            headlines.append(text)

    # Limit to top 10 headlines
    return headlines[:10]

# Start / help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Hello! I can give you the latest news headlines.\nSend /getnews to get the news."
    )

# Command to get news
@bot.message_handler(commands=['getnews'])
def send_news(message):
    headlines = get_headlines()
    if headlines:
        bot.send_message(message.chat.id, "\n\n".join(headlines))
    else:
        bot.send_message(message.chat.id, "Sorry, I couldn't fetch news right now.")

# Keep bot running
bot.polling()
