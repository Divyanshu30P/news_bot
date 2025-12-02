import os
import requests
import telebot

# Read Telegram token and NewsAPI key from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

# Function to get top headlines
def get_headlines():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])
        headlines = [article["title"] for article in articles if article.get("title")]
        return headlines[:10]  # return top 10 headlines
    except Exception as e:
        print("Error fetching news:", e)
        return []

# Start / help command
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "📰 Hello! I can give you the latest news headlines from India.\n"
        "Send /getnews to get the top news!"
    )

# Get news command
@bot.message_handler(commands=["getnews"])
def send_news(message):
    headlines = get_headlines()
    if headlines:
        bot.send_message(message.chat.id, "\n\n".join(headlines))
    else:
        bot.send_message(message.chat.id, "Sorry, I couldn't fetch news right now.")

# Keep bot running
bot.polling()
