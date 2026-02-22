import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

balance = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Финансовый бот запущен\n\n"
        "/add 1000 — добавить деньги\n"
        "/balance — баланс"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global balance
    amount = int(context.args[0])
    balance += amount
    await update.message.reply_text(f"Добавлено {amount} ₽")


async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Баланс: {balance} ₽")


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("balance", get_balance))

app.run_polling()
