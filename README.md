
# Twitch to Telegram Live Stream Notifier

This bot monitors a specified Twitch channel and notifies a Telegram channel when the stream goes live or stops streaming.

## Features
- Automatically fetches the Twitch access token.
- Checks the live status of a specified Twitch channel at regular intervals.
- Notifies a Telegram channel when the specified Twitch stream starts and stops.

## Prerequisites
- Python 3.8+
- Telegram Bot token from [Telegram BotFather](https://core.telegram.org/bots#botfather).
- Twitch Client ID and Client Secret from the [Twitch Developer Portal](https://dev.twitch.tv/console).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   cd YOUR_REPOSITORY_NAME
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project directory with the following environment variables:

   ```env
   TWITCH_CLIENT_ID='your_twitch_client_id'
   TWITCH_CLIENT_SECRET='your_twitch_client_secret'
   TELEGRAM_TOKEN='your_telegram_bot_token'
   ```

## Configuration

Update the placeholders in `twitchannounceintelegram.py`:
- Replace `YOUR_TARGET_CHANNEL_NAME` with the name of the Twitch channel you want to monitor.
- Replace `@YOUR_CHANNEL_ID` with your actual Telegram channel ID (ensure the bot has admin privileges in this channel).

## Usage

Run the bot:
```bash
python twitchannounceintelegram.py
```

## How It Works

- The bot will check the live status of the specified Twitch channel every 5 minutes.
- If the stream goes live, it sends a notification to the Telegram channel.
- If the stream stops, it will also notify the channel.

## License

This project is licensed under the MIT License.
