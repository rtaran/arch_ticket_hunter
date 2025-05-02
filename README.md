# Arch Ticket Hunter

A bot that monitors ticket availability for the Archstoyanie Festival and sends Telegram notifications when tickets become available.

## Description

Arch Ticket Hunter is a simple Python bot that periodically checks a specific URL for ticket availability to the Archstoyanie Festival. When tickets become available, it sends a notification via Telegram to alert the user.

## Features

- Checks ticket availability every 5 minutes
- Sends Telegram notifications when tickets are available
- Includes a simple Flask web server to keep the bot alive when hosted on platforms like Replit

## Requirements

- Python 3.12 or higher
- Dependencies:
  - Beautiful Soup 4
  - python-dotenv
  - Flask
  - Requests

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

3. Create a `.env` file in the project root with the following variables:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   CHAT_ID=your_telegram_chat_id
   ```

## Usage

Run the bot:
```
python main.py
```

The bot will start checking for ticket availability every 5 minutes and will send a Telegram message when tickets become available.

## Deployment

This bot can be deployed on platforms like Replit or Render. The included Flask web server helps keep the bot alive on these platforms.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.