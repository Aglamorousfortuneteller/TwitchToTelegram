import requests
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram import Update

# Twitch API Parameters / Параметры Twitch API
TWITCH_CLIENT_ID = 'YOUR_TWITCH_CLIENT_ID'  # Replace with your Twitch Client ID / Замените на ваш Twitch Client ID
TWITCH_CLIENT_SECRET = 'YOUR_TWITCH_CLIENT_SECRET'  # Replace with your Twitch Client Secret / Замените на ваш Twitch Client Secret
TWITCH_ACCESS_TOKEN = None  # Token will be updated dynamically / Токен будет обновляться динамически

# Telegram Bot Parameters / Параметры Telegram бота
TELEGRAM_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'  # Replace with your Telegram Bot Token / Замените на ваш токен Telegram бота
CHANNEL_ID = '@YOUR_CHANNEL_ID'  # Replace with your Telegram channel ID / Замените на ваш ID канала

# Twitch API URLs / URL-адреса Twitch API
TWITCH_API_TOKEN_URL = 'https://id.twitch.tv/oauth2/token'
TWITCH_API_USERS_URL = "https://api.twitch.tv/helix/users"
TWITCH_API_STREAMS_URL = "https://api.twitch.tv/helix/streams"

# Variable for tracking streaming status (initially set to False) / Переменная для отслеживания статуса стрима (по умолчанию False)
is_streaming = False

def get_access_token():
    """
    Get a new access token from Twitch API.
    Получение нового access_token от Twitch API.
    """
    global TWITCH_ACCESS_TOKEN
    params = {
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(TWITCH_API_TOKEN_URL, params=params)
    
    if response.status_code == 200:
        TWITCH_ACCESS_TOKEN = response.json()['access_token']
        print("Token successfully updated!")  # Token successfully updated / Токен обновлен успешно!
    else:
        print(f"Error fetching token: {response.status_code}")  # Error during token request / Ошибка при получении токена

def get_headers():
    """
    Create headers with the updated access token.
    Создание заголовков с обновленным токеном.
    """
    return {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_ACCESS_TOKEN}'
    }

def get_channel_id_by_name(channel_name):
    """
    Get channel ID by the channel's name.
    Получение ID канала по имени канала.
    """
    headers = get_headers()
    params = {
        'login': channel_name
    }
    response = requests.get(TWITCH_API_USERS_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]['id'], data['data'][0]['display_name']
        else:
            print(f"Channel {channel_name} not found.")  # Channel not found / Канал не найден
            return None, None
    else:
        print(f"Error fetching channel ID: {response.status_code}")  # Error during channel ID request / Ошибка при получении ID канала
        return None, None

def check_stream_status(channel_id):
    """
    Check if the stream is live.
    Проверка, идет ли стрим.
    """
    headers = get_headers()
    params = {
        'user_id': channel_id
    }
    response = requests.get(TWITCH_API_STREAMS_URL, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        return len(data['data']) > 0  # Return True if the stream is live / Вернем True, если стрим идет
    else:
        print(f"Error requesting Twitch API: {response.status_code}")  # Error in Twitch API request / Ошибка при запросе к Twitch API
        return False

async def check_and_notify(context: CallbackContext):
    """
    Check stream status and send notifications.
    Проверка статуса стрима и отправка уведомлений.
    """
    global is_streaming
    channel_id, display_name = context.job.data  # Retrieve channel_id and display_name from job data / Получаем channel_id и display_name из данных job

    if channel_id:
        is_live = check_stream_status(channel_id)
        if is_live and not is_streaming:
            # Notify when the stream starts / Уведомление, когда стрим начинается
            await context.bot.send_message(chat_id=CHANNEL_ID, text=f"{display_name} is live on Twitch! Watch here: https://www.twitch.tv/{display_name}")
            is_streaming = True  # Set flag indicating streaming is live / Устанавливаем флаг, что стрим идет
        elif not is_live and is_streaming:
            print(f"{display_name} is no longer streaming.")  # Notify when the stream ends / Сообщение, когда стрим заканчивается
            is_streaming = False  # Reset flag / Сбрасываем флаг
    else:
        print("Error: Channel ID not found.")  # Channel ID error / Ошибка ID канала

async def start_command(update: Update, context: CallbackContext):
    """
    Start command for the bot.
    Команда /start для бота.
    """
    await update.message.reply_text("Bot started and monitoring stream status.")  # Bot started notification / Бот запущен и отслеживает статус стрима

if __name__ == "__main__":
    # Twitch channel to monitor / Twitch канал для отслеживания
    TARGET_CHANNEL_NAME = 'YOUR_TARGET_CHANNEL_NAME'  # Replace with the Twitch channel name to monitor / Замените на имя Twitch канала для отслеживания

    # Get initial access token / Получаем начальный токен доступа
    get_access_token()

    # Retrieve channel ID by name / Получаем ID канала по имени
    TWITCH_CHANNEL_ID, TWITCH_CHANNEL_DISPLAY_NAME = get_channel_id_by_name(TARGET_CHANNEL_NAME)

    if TWITCH_CHANNEL_ID:
        # Create Application object / Создаем объект Application
        application = Application.builder().token(TELEGRAM_TOKEN).build()

        # Schedule a periodic job to check stream status every 5 minutes / Планируем периодическую проверку статуса стрима каждые 5 минут
        job_queue = application.job_queue
        job_queue.run_repeating(check_and_notify, interval=300, first=10, data=(TWITCH_CHANNEL_ID, TWITCH_CHANNEL_DISPLAY_NAME))

        # Add command handler for /start / Добавляем обработчик команды /start
        application.add_handler(CommandHandler("start", start_command))

        # Run the bot / Запуск бота
        application.run_polling()
    else:
        print("Specified channel not found.")  # Channel not found message / Сообщение, если канал не найден
