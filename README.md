### 📄 `README.md`

# 🤖 Steem Witness Telegram Bot

A Python-based Telegram bot that monitors missed blocks by selected Steem witnesses and provides real-time updates via Telegram. It also supports fetching witness stats like rank, produced/missed blocks, and last confirmed block.

## Features

- Sends live alerts when a watched witness misses a block
- `/ping` command to check if the bot is running
- `/info` command to get current stats of `Your Witness id`
- Clean, readable timestamps (12-hour format with AM/PM)
- Runs continuously via Docker or on VPS
- Minimal resource usage

##  Requirements

- Python 3.10+
- Telegram Bot Token
- Docker (optional, but recommended for deployment)

## Setup (Local or VPS)

1. **Clone this repo** or upload the files to your server
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt


3. **Configure the bot**:

   * Edit `bot.py` and replace:

     * `BOT_TOKEN` with your Telegram bot token
     * `USER_ID` with your Telegram user ID

4. **Run the bot**:

   ```bash
   python bot.py
   ```

---

##  Run with Docker

1. **Build the image**:

   ```bash
   docker build -t <your-bot-name> .
   ```

2. **Run the container**:

   ```bash
   docker run -d --restart unless-stopped --name <your-bot-name> <your-bot-name>
   ```


---

## Telegram Commands

* `/ping` – Check if the bot is alive
* `/info` – Get stats for `Your Witness`


## License

MIT License – do whatever you want, just don’t break the Steem blockchain. 😉

---

## ✨ Author

Made with 💙 Dhaka Witness
https://steemit.com/@dhaka.witness
