from decouple import config
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

class ProductDescriptionGenerator:
    def __init__(self):
        # Получение данных из файла конфигурации
        self.client_id = config('client_id', default='')
        self.secret = config('secret', default='')
        self.auth = config('auth', default='')
        # Инициализация GigaChat с указанием credentials
        self.giga = GigaChat(credentials=self.auth,
                             model='GigaChat:latest',
                             verify_ssl_certs=False)

    def generate_description(self, product_names, keywords=None):
        # Определение сообщений для генерации описания товара
        system_message = SystemMessage(
            content='''Ты - опытный составитель описаний для справочника номенклатуры в 1С УТ 11.
              Твоя задача -  создать полное и информативное описание товара,
              включая его характеристики, преимущества, применение и другие важные детали,
              но в формате, подходящем для справочника номенклатуры 1С УТ 11.
              Избегай рекламных фраз,  фокусируйся на объективной информации'''
        )

        if keywords:
            keywords_str = ", ".join(keywords)
        else:
            keywords_str = ""

        descriptions = []
        for product_name in product_names:
            human_message = HumanMessage(
                content=f'''Название товара: {product_name}.
                           Ключевые слова: {keywords_str}.
                           Укажи описание номенклатуры или товара в один хороший абзац.'''
            )

            # Запрос к GigaChat с использованием определенных сообщений
            response = self.giga([system_message, human_message])
            descriptions.append(response.content)

        # Вывод результата
        return descriptions

# Пример использования класса
generator = ProductDescriptionGenerator()
product_names = ["Шоколад Милка", "Чай Lipton"]
keywords = ["Вкус", "Качество"]
descriptions = generator.generate_description(product_names, keywords=keywords)
for description in descriptions:
    print(description)
