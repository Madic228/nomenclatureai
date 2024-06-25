import json
import uuid
import requests
from bs4 import BeautifulSoup
from decouple import config

class TokenManager:
    def __init__(self, auth_token, scope='GIGACHAT_API_PERS'):
        self.auth_token = auth_token
        self.scope = scope
        self.giga_token = None

    def get_token(self):
        """
        Выполняет POST-запрос к эндпоинту, который выдает токен.

        Возвращает:
        - ответ API, где токен и срок его "годности".
        """
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
            print(f"Ошибка: {str(e)}")
            return -1
        return self.giga_token


class GigaChatClient:
    def __init__(self, token_manager):
        self.token_manager = token_manager
        self.giga_token = token_manager.giga_token

    def send_chat_request(self, user_message):
        """
        Отправляет POST-запрос к API GigaChat для получения ответа от модели чата.

        Параметры:
        - user_message (str): Сообщение пользователя, которое будет обработано моделью GigaChat.

        Возвращает:
        - str: Строка сгенерированного ответа GigaChat с тэгом img
        """
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
              Твоя задача -  создать простое и понятное изображение товара,
              но в формате, подходящем для справочника номенклатуры 1С УТ 11.
              Избегай большого количества цветов и оттенков, фокусируйся на реальном изображении"""
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
        """
        Скачивает изображение по URL из тега img и сохраняет его в файл.

        Параметры:
        - img_tag (str): HTML-тег img, содержащий URL изображения.
        - output_filename (str): Имя файла для сохранения изображения.
        """
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
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as {output_filename}")
        except requests.RequestException as e:
            print(f"Произошла ошибка при загрузке изображения: {str(e)}")


# Инициализация менеджера токенов и клиента GigaChat
client_id = config('CLIENT_ID', default='')
secret = config('SECRET', default='')
auth = config('AUTH', default='')
token_manager = TokenManager(auth)
token_manager.get_token()

if token_manager.giga_token:
    giga_chat_client = GigaChatClient(token_manager)
    user_message = "Нарисуй соковыжималку"
    response_img_tag = giga_chat_client.send_chat_request(user_message)
    if response_img_tag:
        giga_chat_client.download_image(response_img_tag, 'image.jpg')
else:
    print("Не удалось получить токен.")
