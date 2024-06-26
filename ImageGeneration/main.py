import json
import uuid
import requests
from bs4 import BeautifulSoup
from decouple import config
import base64

class TokenManager:
    def __init__(self, auth_token, scope='GIGACHAT_API_PERS'):
        self.auth_token = auth_token
        self.scope = scope
        self.giga_token = None

    def get_token(self):
        """
        Выполняет POST-запрос к эндпоинту, который выдает токен.

        Возвращает:
        - токен (str): Токен авторизации.
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
            return None
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
        - str: Строка сгенерированного ответа GigaChat с тэгом img.
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
        """
        Скачивает изображение по URL из тега img, сохраняет его в файл и конвертирует в base64.

        Параметры:
        - img_tag (str): HTML-тег img, содержащий URL изображения.
        - output_filename (str): Имя файла для сохранения изображения.

        Возвращает:
        - str: Изображение в формате base64.
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

            # Конвертируем изображение в base64
            with open(output_filename, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
        except requests.RequestException as e:
            print(f"Произошла ошибка при загрузке изображения: {str(e)}")
            return None


class ProductImageGeneration:
    def __init__(self):
        auth = "NTdlOGY2NWEtODY5OS00M2I3LWE3MmEtMGQyNzQ5MDEzNThhOmI4MjZhMzZmLWIwMDEtNDkzYi05MzhkLTZmMmZlOGY1YTYwZA=="
        # auth = config('AUTH', default='')
        self.token_manager = TokenManager(auth)
        self.token_manager.get_token()
        self.giga_chat_client = GigaChatClient(self.token_manager) if self.token_manager.giga_token else None

    def run(self):
        if not self.giga_chat_client:
            print("Не удалось получить токен.")
            return None

        product_names = [
            "Нарисуй деревенское сливочное масло",
            "Нарисуй деревенское сливочное масло",
            "Нарисуй деревенское сливочное масло",
            "Нарисуй деревенское сливочное масло"
        ]

        base64_images = []

        for i, user_message in enumerate(product_names):
            response_img_tag = self.giga_chat_client.send_chat_request(user_message)
            if response_img_tag:
                output_filename = f'image_{i + 1}.jpg'
                base64_image = self.giga_chat_client.download_image(response_img_tag, output_filename)
                if base64_image:
                    base64_images.append((user_message, base64_image))
                    print(f"Base64 encoded image {i + 1}:")
                    print(base64_image)

        return base64_images


# # Запуск основной функции и получение результатов
# giga_chat_service = ProductImageGeneration()
# base64_images = giga_chat_service.run()
# if base64_images:
#     for user_message, base64_image in base64_images:
#         print(f"Request: {user_message}")
#         print(f"Base64: {base64_image}")
