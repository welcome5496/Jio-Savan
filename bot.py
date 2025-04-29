import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Your bot token (use with caution)
BOT_TOKEN = "8157582382:AAGgIhtU_jmzK24bqjCDSfOnl6Y5hPtEEdo"

async def search_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Usage: /song <song name>")
        return

    url = f"https://saavn.dev/api/search/songs?query={query}"
    response = requests.get(url)
    data = response.json()

    if data['data']['results']:
        song = data['data']['results'][0]
        message = (
            f"**{song['name']}**\n"
            f"Artist: {', '.join(song['primaryArtists'].split(', '))}\n"
            f"[Listen Here]({song['url']})"
        )
        await update.message.reply_photo(photo=song['image'][2]['link'], caption=message, parse_mode='Markdown')
    else:
        await update.message.reply_text("No song found.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("song", search_song))
app.run_polling()
