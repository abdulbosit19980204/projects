from django.test import TestCase
import requests

# Create your tests here.
BOT_TOKEN = '6189703946:AAGb1TA2yDg-sdu0c_AIDn39_07AuzvlZgE'
CHAT_ID = '1209619850'
TEXT = 'hello'
url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={TEXT}'
response = requests.get(url)
print(response)
