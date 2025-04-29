import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# Enable logging for better error tracking
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8157582382:AAGgIhtU_jmzK24bqjCDSfOnl6Y5hPtEEdo"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Creating inline button for song search
    keyboard = [
        [InlineKeyboardButton("Search Songs", callback_data='search_song')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Click below to search for songs.", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'search_song':
        # Send a message asking for song query
        await query.message.reply_text("Please type the song name you want to search.")

async def search_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.message.text
        if not query:
            await update.message.reply_text("Usage: Just type the song name")
            return

        url = f"https://saavn.dev/api/search/songs?query={query}"
        response = requests.get(url)
        
        # Log the raw API response
        logger.debug(f"API Response: {response.text}")
        
        data = response.json()

        if 'data' in data and 'results' in data['data'] and data['data']['results']:
            song = data['data']['results'][0]
            message = (
                f"**{song['name']}**\n"
                f"Artist: {', '.join(song['primaryArtists'].split(', '))}\n"
                f"[Listen Here]({song['url']})"
            )
            await update.message.reply_photo(photo=song['image'][2]['link'], caption=message, parse_mode='Markdown')
        else:
            await update.message.reply_text("No song found.")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        await update.message.reply_text("An error occurred while processing the request.")

# Create the bot application and set up command handlers
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_song))

# Start the bot
app.run_polling()
