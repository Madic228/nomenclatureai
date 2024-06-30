from langchain_community.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage
from decouple import config

class NomenclatureDuplicateFinder:
    def __init__(self):
        # self.auth = config('AUTH', default='')
        self.auth = "NTdlOGY2NWEtODY5OS00M2I3LWE3MmEtMGQyNzQ5MDEzNThhOmI4MjZhMzZmLWIwMDEtNDkzYi05MzhkLTZmMmZlOGY1YTYwZA=="
        self.giga = GigaChat(credentials=self.auth,
                             model='GigaChat:latest',
                             verify_ssl_certs=False)

    def find_duplicates(self, nomenclature_list):
        system_message = SystemMessage(
            content='''Ты - опытный специалист по работе с номенклатурами.
            Твоя задача - найти дублирующиеся номенклатуры в списке.
            Верни список дубликатов, если таковые имеются.'''
        )

        human_message = HumanMessage(
            content=f'''Вот список номенклатур: {nomenclature_list}.
            Определи и верни список дубликатов.'''
        )

        try:
            response = self.giga([system_message, human_message])
        except Exception as e:
            print(f"Ошибка при запросе к GigaChat: {e}")
            return []

        duplicates = response.content.strip()
        return duplicates

# Пример использования

import json

# Загрузка списка номенклатур из JSON файла
# Загрузка списка номенклатур из JSON файла
with open('Nomenklatura.json', 'r', encoding='utf-8') as file:
    nomenclature_list = json.load(file)

duplicate_finder = NomenclatureDuplicateFinder()
duplicates = duplicate_finder.find_duplicates(nomenclature_list)
print("Найденные дубликаты:", duplicates)