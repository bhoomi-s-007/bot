from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from collections import defaultdict

# Replace these with your Bot Token, Log Channel ID, and your Telegram ID
BOT_TOKEN = '7507821106:AAF1e07OSYaatMJYMKM0Sr5cBAcU6BwCm1A'
LOG_CHANNEL_ID = '-1002273435527'
YOUR_TELEGRAM_ID = '1822190035'

# Simple in-memory dictionary to track user balances (for demonstration purposes)
user_balances = defaultdict(int)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /start command with an introductory message and inline buttons."""
    user = update.message.from_user

    # If the start command is from the owner, display their balance
    if user.id == YOUR_TELEGRAM_ID:
        balance = user_balances[user.id]
        await update.message.reply_text(f"Welcome back! You currently have {balance} stars. ⭐️")
    else:
        message = (
            "We have different payment plans available for you.\n\n"
            "🎁 BUY MORE, GET MORE! 🎁\n\n"
            "🆘 For Help & Support, CONTACT\n"
            "🆔 @I_am_DarkKnight ✅\n\n"
            "BUY COINs WITH TG STARs"
        )

        # Define inline keyboard buttons for different star packages
        keyboard = [
            [InlineKeyboardButton("500 Stars", callback_data="buy_500")],
            [InlineKeyboardButton("1000 Stars", callback_data="buy_1000")],
            [InlineKeyboardButton("2000 Stars", callback_data="buy_2000")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the welcome message with the inline buttons
        await update.message.reply_text(message, reply_markup=reply_markup)

    # Log the user's start to the log channel
    log_message = f"User started the bot:\nUsername: @{user.username}\nUser ID: {user.id}"
    await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_message)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles button callbacks for different star packages."""
    query = update.callback_query
    await query.answer()

    # Determine which package was selected and add stars to the user's balance
    if query.data == "buy_500":
        await process_stars_purchase(query.message.chat_id, context, "500 Stars", 500)
    elif query.data == "buy_1000":
        await process_stars_purchase(query.message.chat_id, context, "1000 Stars", 1000)
    elif query.data == "buy_2000":
        await process_stars_purchase(query.message.chat_id, context, "2000 Stars", 2000)

async def process_stars_purchase(chat_id, context: ContextTypes.DEFAULT_TYPE, title, stars) -> None:
    """Simulates a stars purchase by updating user balance and logging the transaction."""
    # Add stars to the user's balance
    user_id = chat_id
    user_balances[user_id] += stars

    # Log the purchase to the log channel
    log_message = f"User made a stars purchase:\nUser ID: {user_id}\nPurchased: {title}\nNew Balance: {user_balances[user_id]} stars"
    await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_message)

    # Send confirmation to the user
    await context.bot.send_message(chat_id=chat_id, text=f"Thank you for purchasing {title}! You now have {user_balances[user_id]} stars.")

async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the /terms command with non-refundable payment terms."""
    terms_message = (
        "Please note: All payments are final and non-refundable.\n"
        "Before proceeding with any payment, please contact @I_am_DarkKnight "
        "for assistance to ensure a smooth transaction."
    )
    await update.message.reply_text(terms_message)

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Allows users to check their current star balance."""
    user_id = update.message.from_user.id
    balance = user_balances[user_id]
    await update.message.reply_text(f"You currently have {balance} stars! ⭐️")

def main() -> None:
    # Set up the application and dispatcher
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("terms", terms))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
