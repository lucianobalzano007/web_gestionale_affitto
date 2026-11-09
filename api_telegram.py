import requests
import os

def send_message(chat_id,message):
    token=os.getenv('BOT_TOKEN')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    json={
        'text': message,
        'chat_id': str(chat_id),
        'parse_mode':'HTML',
    }
    response=requests.post(url=url,json=json)
    if response.status_code != 200:
        print(f"Errore Telegram: {response.text}")
    return response