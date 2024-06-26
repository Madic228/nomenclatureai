from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException, Query
import os
from fastapi.responses import StreamingResponse
from io import BytesIO
import logging
from concurrent.futures import ThreadPoolExecutor
from fastapi.responses import FileResponse
from TextGeneration.ProductDescriptionGenerator import ProductDescriptionGenerator
from TextGeneration.UnitOfMeasurementGenerator import UnitOfMeasurementGenerator
from ImageGeneration.main import ProductImageGeneration
from decouple import config
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()

def log_message(message):
    logging.info(message)

@app.get("/request-test/")
def get_request_test():
    return {"Успешно"}


@app.get("/get-nomenclature-description/{name}")
def get_nomenclature_description(name: str, keywords: str = Query(None)):

    generator = ProductDescriptionGenerator()
    product_names = name.split("|") # Можно передать несколько товаров/номенклатур
    if keywords is not None:
        keywords = keywords.split("|") # Не обязательное поле Ключевые слова
    descriptions = generator.generate_description(product_names, keywords=keywords)
     # Modify the return statement to structure the JSON response
    structured_descriptions = []

    for index, desc in enumerate(descriptions):
        new_desc = desc.replace("\"", '')  # Modify the description (not the tuple)
        structured_descriptions.append({
            "description": new_desc
        })

    return {"descriptions": structured_descriptions}  # Return structured JSON

@app.get("/get-nomenclature-image/{name}")
def get_nomenclature_description(name: str):
    product_name = name
    giga_chat_service = ProductImageGeneration()
    base64_images = giga_chat_service.run(product_name)
    return base64_images

@app.get("/get-nomenclature-measurement/{name}")
def get_nomenclature_description(name: str):

    generator = UnitOfMeasurementGenerator()
    product_names = name.split("|")
    units_of_measurement = generator.generate_units_of_measurement(product_names)
    return {"measurement": units_of_measurement}

# def connect_to_database():
#     try:
#         connection = mysql.connector.connect(
#             host="localhost",
#             user="admin",
#             password="admin",
#             database="tarkov"
#         )
#         log_message("Успешное подключение к базе данных")
#         return connection
#     except Exception as e:
#         log_message(f"Ошибка при подключении к базе данных: {str(e)}")
#         return None

# def fetch_videos():
#     try:
#         connection = connect_to_database()
#         if connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT * FROM videos")
#             videos = cursor.fetchall()
#             connection.close()
#             log_message(f"Получено {len(videos)} видео из базы данных")
#             return videos
#         else:
#             return None
#     except Exception as e:
#         log_message(f"Ошибка при выполнении запроса к базе данных: {str(e)}")
#         return None

# def fetch_request_times():
#     try:
#         connection = connect_to_database()
#         if connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT * FROM request_time_manager")
#             request_times = cursor.fetchall()
#             connection.close()
#             log_message(f"Получено {len(request_times)} времен запросов из базы данных")
#             return request_times
#         else:
#             return None
#     except Exception as e:
#         log_message(f"Ошибка при выполнении запроса к базе данных: {str(e)}")
#         return None

# @app.get("/videos/")
# def get_videos():
#     videos = fetch_videos()
#     if videos:
#         video_list = [{"video_id": video[1], "title": video[2], "publication_date": video[3]} for video in videos]
#         log_message("Получен список видеороликов")
#         return {"videos": video_list}
#     else:
#         return {"message": "Ошибка при получении видеороликов из базы данных"}

# @app.get("/request-times/")
# def get_request_times():
#     request_times = fetch_request_times()
#     if request_times:
#         log_message("Получены запросы времени")
#         return {"request_times": request_times}
#     else:
#         return {"message": "Ошибка при получении времен запросов из базы данных"}

# # Путь к папке с изображениями
# IMAGE_DIRECTORY = "/root/tarkov_api/maps/WoodsMap"

# @app.get("/images/{image_name}")
# async def get_image(image_name: str):
#     image_path = os.path.join(IMAGE_DIRECTORY, image_name)
#     if os.path.exists(image_path):
#         return FileResponse(image_path)
#     else:
#         return {"message": "Изображение не найдено"}rt