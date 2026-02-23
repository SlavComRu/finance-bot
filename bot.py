import os
import json

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

DATA_FILE = "data.json"

# ===== СОСТОЯНИЯ =====
MENU, INCOME_AMOUNT, EXPENSE_AMOUNT, COMMENT = range(4)

# ===== КЛАВИАТУРА =====
keyboard = [
    ["💰 Доход", "➖ Расход"],
    ["📊 Баланс"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)


# ===== БАЗА =====
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"balance": 0, "operations": []}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Финансовый бот готов",
        reply_markup=reply_markup
    )
    return MENU


# ===== МЕНЮ =====
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "💰 Доход":
        await update.message.reply_text("Введите сумму дохода:")
        return INCOME_AMOUNT

    elif text == "➖ Расход":
        await update.message.reply_text("Введите сумму расхода:")
        return EXPENSE_AMOUNT

    elif text == "📊 Баланс":
        data = load_data()
        await update.message.reply_text(
            f"💰 Баланс: {data['balance']}",
            reply_markup=reply_markup
        )
        return MENU

    return MENU


# ===== ДОХОД =====
async def income_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["amount"] = int(update.message.text)
        await update.message.reply_text("Источник дохода?")
        return COMMENT
    except:
        await update.message.reply_text("Введите число")
        return INCOME_AMOUNT


# ===== РАСХОД =====
async def expense_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data["amount"] = -int(update.message.text)
        await update.message.reply_text("Категория расхода?")
        return COMMENT
    except:
        await update.message.reply_text("Введите число")
        return EXPENSE_AMOUNT


# ===== СОХРАНЕНИЕ =====
async def save_operation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()

    amount = context.user_data["amount"]
    comment = update.message.text

    data["balance"] += amount
    data["operations"].append({
        "amount": amount,
        "comment": comment
    })

    save_data(data)

    await update.message.reply_text(
        f"✅ Сохранено\n{amount} | {comment}\n💰 Баланс: {data['balance']}",
        reply_markup=reply_markup
    )

    return MENU


# ===== ЗАПУСК =====
app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
        INCOME_AMOUNT: [MessageHandler(filters.TEXT, income_amount)],
        EXPENSE_AMOUNT: [MessageHandler(filters.TEXT, expense_amount)],
        COMMENT: [MessageHandler(filters.TEXT, save_operation)],
    },
    fallbacks=[CommandHandler("start", start)],
)

app.add_handler(conv_handler)

print("BOT STARTED")

app.run_polling()
