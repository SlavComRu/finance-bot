import os
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "data.json"


# ===== база =====
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"balance": 0, "operations": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ===== команды =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Финансовый бот готов\n\n"
        "Добавить доход:\n"
        "/add +1000 зарплата\n\n"
        "Добавить расход:\n"
        "/add -500 продукты"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()

    try:
        amount = int(context.args[0])
        comment = " ".join(context.args[1:])
    except:
        await update.message.reply_text("Ошибка.\nПример: /add -500 еда")
        return

    data["balance"] += amount
    data["operations"].append({
        "amount": amount,
        "comment": comment
    })

    save_data(data)

    await update.message.reply_text(
        f"✅ Записано: {amount}\n"
        f"💬 {comment}\n"
        f"💰 Баланс: {data['balance']}"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    await update.message.reply_text(f"💰 Баланс: {data['balance']}")


# ===== запуск =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("balance", balance))

app.run_polling()
