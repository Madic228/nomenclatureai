import json
import uuid
import requests
from bs4 import BeautifulSoup
from decouple import config
import base64
import time

class TokenManager:
    def __init__(self, auth_token, scope='GIGACHAT_API_PERS'):
        self.auth_token = auth_token
        self.scope = scope
        self.giga_token = None

    def get_token(self):
        rq_uid = str(uuid.uuid4())
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': rq_uid,
            'Authorization': f'Basic {self.auth_token}'
        }
        payload = {'scope': self.scope}
        try:
            response = requests.post(url, headers=headers, data=payload, verify=False)
            response.raise_for_status()
            self.giga_token = response.json().get('access_token')
        except requests.RequestException as e:
            print(f"Ошибка при создании токена: {str(e)}")
            self.giga_token = None
        return self.giga_token

class GigaChatClient:
    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.giga_token = token_manager.giga_token

    def send_chat_request(self, user_message):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.giga_token}',
        }
        payload = {
            "model": "GigaChat:latest",
            "messages": [
                {
                    "role": "system",
                    "content": """Ты - опытный дизайнер изображений для справочника номенклатуры в 1С УТ 11.
                    Твоя задача - создать простое и понятное изображение товара,
                    но в формате, подходящем для справочника номенклатуры 1С УТ 11.
                    Избегай большого количества цветов и оттенков, фокусируйся на реальном изображении."""
                },
                {
                    "role": "user",
                    "content": user_message
                },
            ],
            "function_call": "auto",
        }
        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except requests.RequestException as e:
            print(f"Произошла ошибка: {str(e)}")
            return None

    def download_image(self, img_tag, output_filename):
        soup = BeautifulSoup(img_tag, 'html.parser')
        img_src = soup.img['src']
        url = f'https://gigachat.devices.sberbank.ru/api/v1/files/{img_src}/content'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.giga_token}',
        }
        try:
            response = requests.get(url, headers=headers, verify=False)
            response.raise_for_status()
            encoded_string = base64.b64encode(response.content).decode('utf-8')
            return encoded_string
        except requests.RequestException as e:
            print(f"Произошла ошибка при загрузке изображения: {str(e)}")
            return None

class ProductImageGeneration:
    def __init__(self):
        auth = config('AUTH', default='')
        self.token_manager = TokenManager(auth)
        self.obtain_token()
        self.giga_chat_client = GigaChatClient(self.token_manager) if self.token_manager.giga_token else None

    def obtain_token(self):
        for _ in range(3):  # 3 попытки получения токена при сбое
            token = self.token_manager.get_token()
            if token:
                break
            print("Не удалось получить токен, повторная попытка...")
            time.sleep(2)  # Ожидание 2 секунды между попытками

    def run(self, product_name):
        if not self.giga_chat_client:
            print("Не удалось получить токен.")
            return None

        pr = f"Нарисуй {product_name}"
        product_names = [
            pr,
            pr,
            pr,
            pr
        ]

        base64_images = []

        for i, user_message in enumerate(product_names):
            response_img_tag = self.giga_chat_client.send_chat_request(user_message)
            if response_img_tag:
                output_filename = f'image_{i + 1}.jpg'
                base64_image = self.giga_chat_client.download_image(response_img_tag, output_filename)
                if base64_image:
                    base64_images.append((user_message, base64_image))

        return base64_images

# Запуск основной функции и получение результатов
giga_chat_service = ProductImageGeneration()
product_name = "деревенское сливочное масло"
base64_images = giga_chat_service.run(product_name)
if base64_images:
    for user_message, base64_image in base64_images:
        print(f"Запрос: {user_message} \n Изображение закодировано.")
        # print(f"Кодировка: {base64_image}")
