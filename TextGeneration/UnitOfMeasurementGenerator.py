# from decouple import config
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

class UnitOfMeasurementGenerator:
    def __init__(self):
        # Инициализация GigaChat для генерации единиц измерения
        # self.auth = config('auth', default='')
        self.auth = "NTdlOGY2NWEtODY5OS00M2I3LWE3MmEtMGQyNzQ5MDEzNThhOmI4MjZhMzZmLWIwMDEtNDkzYi05MzhkLTZmMmZlOGY1YTYwZA=="
        self.giga = GigaChat(credentials=self.auth,
                             model='GigaChat:latest',
                             verify_ssl_certs=False)

    def generate_units_of_measurement(self, product_names):
        # Определение системного сообщения для генерации единиц измерения
        system_message = SystemMessage(
            content='''Ты - опытный специалист по номенклатуре и единицам измерения.
              Твоя задача - определить единицу измерения для каждой номенклатуры.
              Укажи единицу измерения для каждой номенклатуры.'''
        )

        # Генерация единиц измерения для каждого названия товара
        units_of_measurement = []
        for product_name in product_names:
            human_message = HumanMessage(
                content=f'''Название товара: {product_name}.
                           Укажи единицу измерения для этой номенклатуры. Верни только ЕДИНИЦУ ИЗМЕРЕНИЯ И НИЧЕГО БОЛЕЕ'''
            )

            # Запрос генерации единицы измерения у GigaChat
            response = self.giga([system_message, human_message])
            units_of_measurement.append(response.content)

        return units_of_measurement

# # Пример использования
# generator = UnitOfMeasurementGenerator()
# product_names = ["Вода", "Мука", "Молоко", 'подшибники', 'Коферка BOSTON']
# units_of_measurement = generator.generate_units_of_measurement(product_names)
# for unit in units_of_measurement:
#     print(unit)
