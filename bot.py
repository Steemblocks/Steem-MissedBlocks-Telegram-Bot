import requests
import asyncio
import sys
import nest_asyncio
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# === CONFIG ===
BOT_TOKEN = "Bot Token"  # Replace with your actual bot token
USER_ID = Telegram User Id
WATCHED_WITNESSES = {
    "Your Witness Id"
}
API_URL = "https://sds0.steemworld.org/witnesses_api/getRecentlyMissedBlocks"
notified_events = set()  # To avoid duplicate alerts

# === Time formatting helpers ===
def day_suffix(day):
    if 11 <= day <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

def format_timestamp(ts):
    dt = datetime.utcfromtimestamp(ts)
    suffix = day_suffix(dt.day)
    return dt.strftime(f"%I:%M:%S %p, {dt.day}{suffix} %B, %Y")

# === /ping command ===
async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("[PING] Bot received /ping command.")
    await update.message.reply_text("✅ I'm alive and watching missed blocks!")

# === /info command ===
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        witness_name = "dhaka.witness"
        print(f"[INFO] Fetching witness stats for {witness_name}")
        url = f"https://sds.steemworld.org/witnesses_api/getWitnessStats/{witness_name}"
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()["result"]

        msg = (
            f"ℹ️ Witness Info:\n"
            f"Rank: {data['rank']}\n"
            f"Produced Blocks: {data['produced_blocks']:,}\n"
            f"Missed Blocks: {data['missed_blocks']:,}\n"
            f"Last Confirmed Block: {data['last_confirmed_block']}"
        )
        print(f"[INFO] Rank: {data['rank']}, Produced: {data['produced_blocks']}, Missed: {data['missed_blocks']}")
        await update.message.reply_text(msg)

    except Exception as e:
        print("❌ Error fetching /info:", e)
        await update.message.reply_text("⚠️ Failed to fetch witness info.")

# === Check missed blocks ===
async def check_missed_blocks(bot: Bot):
    global notified_events
    try:
        res = requests.get(API_URL)
        res.raise_for_status()
        data = res.json()["result"]["rows"]

        new_events = [
            (timestamp, witness)
            for timestamp, witness in data
            if witness in WATCHED_WITNESSES and (timestamp, witness) not in notified_events
        ]

        for timestamp, witness in new_events:
            formatted_time = format_timestamp(timestamp)
            msg = f"🚨 {witness} missed 1 block ({formatted_time})"
            print(f"[MISSED] {witness} missed 1 block at {formatted_time}")
            await bot.send_message(chat_id=USER_ID, text=msg)
            notified_events.add((timestamp, witness))

    except Exception as e:
        print("❌ Error checking missed blocks:", e)

# === Background task to keep checking ===
async def periodic_check(bot: Bot):
    while True:
        await check_missed_blocks(bot)
        await asyncio.sleep(10)

# === Bot setup ===
def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("info", info))

    print("✅ Bot is running... Type /ping or /info in Telegram.")

    loop = asyncio.get_event_loop()
    loop.create_task(periodic_check(app.bot))

    app.run_polling()

# === Start everything ===
if __name__ == "__main__":
    nest_asyncio.apply()
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run_bot()
