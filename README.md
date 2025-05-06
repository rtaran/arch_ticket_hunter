# Arch Ticket Hunter

A bot that monitors ticket availability for the Archstoyanie Festival and sends Telegram notifications when tickets become available.

## Description

Arch Ticket Hunter is a Python bot that periodically checks for ticket availability to the Archstoyanie Festival. It features a Telegram interface with buttons for control and sends regular status reports.

## Features

- Interactive Telegram bot with control buttons
- Regular status reports every 3 hours (configurable)
- On-demand ticket availability checks
- Ability to pause and resume the bot
- Sends Telegram notifications when tickets become available

## Requirements

- Python 3.8 or higher
- Dependencies:
  - Beautiful Soup 4
  - python-dotenv
  - python-telegram-bot
  - Requests
  - Schedule

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/arch-ticket-hunter.git
   cd arch-ticket-hunter
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root using the template:
   ```
   cp .env.template .env
   ```

4. Edit the `.env` file with your Telegram bot token and chat ID:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   STATUS_INTERVAL_HOURS=3
   ```

## Usage

1. Run the bot:
   ```
   python main.py
   ```

2. The bot will start and send you a welcome message in Telegram with control buttons.

3. Available commands:
   - `/start` - Start the bot and show control buttons
   - `/status` - Check current ticket status
   - `/controls` - Show control buttons
   - `/help` - Show help message

4. Control buttons:
   - **Check Now** - Perform an immediate ticket availability check
   - **Status** - Get the current status report
   - **Pause Bot** - Pause automatic status reports
   - **Resume Bot** - Resume automatic status reports

## Deployment

This bot can be deployed on platforms like Render. The provided `render.yaml` file helps with configuration.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.