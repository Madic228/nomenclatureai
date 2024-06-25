import json
import uuid
import requests
from bs4 import BeautifulSoup

auth = "ZGEzMDdlZWYtZGFjYi00OWY2LWFkNDMtODg5NWM0MDRjZTFjOjI3MDUyMWIyLTE3ZjctNGJhMy1iNWY2LWUxNTRmODdmNTBmNg=="

def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.

      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - область (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        # Делаем POST запрос с отключенной SSL верификацией
        # (можно скачать сертификаты Минцифры, тогда отключать проверку не надо)
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1


response = get_token(auth)
if response != 1:
    print(response.text)
    giga_token = response.json()['access_token']

def send_chat_request(giga_token, user_message):
    """
    Отправляет POST-запрос к API GigaChat для получения ответа от модели чата.

    Параметры:
    - giga_token (str): Токен авторизации для доступа к API GigaChat.
    - user_message (str): Сообщение пользователя, которое будет обработано моделью GigaChat.

    Возвращает:
    - str: Строка сгенерированного ответа GigaChat с тэгом img
    """
    # URL API для отправки запросов к GigaChat
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Заголовки для HTTP-запроса
    headers = {
        'Content-Type': 'application/json',  # Указываем, что отправляемые данные в формате JSON
        'Authorization': f'Bearer {giga_token}',  # Используем токен авторизации для доступа к API
    }

    # Данные для отправки в теле запроса
    payload = {
        "model": "GigaChat:latest",  # Указываем, что хотим использовать последнюю версию модели GigaChat
        "messages": [
            {
                "role": "user",  # Роль отправителя - пользователь
                "content": user_message  # Сообщение от пользователя
            },
        ],
        "function_call": "auto",
    }

    try:
        # Отправляем POST-запрос к API и получаем ответ
        response = requests.post(url, headers=headers, data=json.dumps(payload), verify=False)
        # Выводим текст ответа. В реальных условиях следует обрабатывать ответ и проверять статус коды.
        print(response.json())
        return response.json()["choices"][0]["message"]["content"]
    except requests.RequestException as e:
        # В случае возникновения исключения в процессе выполнения запроса, выводим ошибку
        print(f"Произошла ошибка: {str(e)}")
        return None


user_message = "Нарисуй шоколадную плитку с названием Milka, реальное фото"
response_img_tag = send_chat_request(giga_token, user_message)
print(response_img_tag)

# Парсим HTML
soup = BeautifulSoup(response_img_tag, 'html.parser')

# Извлекаем значение атрибута `src`
img_src = soup.img['src']

print(img_src)

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {giga_token}',
}

response = requests.get(f'https://gigachat.devices.sberbank.ru/api/v1/files/{img_src}/content', headers=headers,
                        verify=False)

with open('image.jpg', 'wb') as f:
    f.write(response.content)
