from decouple import config
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

# Получение данных из файла конфигурации
client_id = config('client_id', default='')
secret = config('secret', default='')
auth = config('auth', default='')

# Инициализация GigaChat с указанием credentials
giga = GigaChat(credentials=auth,
                model='GigaChat:latest',
                verify_ssl_certs=False)

# Определение сообщений для генерации описания товара
system_message = SystemMessage(
    content='''Ты — профессиональный маркетолог с опытом написания высококонверсионной рекламы. 
               Для генерации описания товара ты изучаешь потенциальную целевую аудиторию и оптимизируешь 
               рекламный текст так, чтобы он обращался именно к этой целевой аудитории. 
               Создай текст описания номенклатуры, 
               который побуждает пользователей к целевому действию. Добавьте здесь больше контекста о товаре, 
               его особенностях, преимуществах и других важных деталях.'''
)

human_message = HumanMessage(
    content='''Название товара: Транзистор. 
               Добавьте здесь дополнительные детали о товаре, его характеристиках, преимуществах и 
               других важных аспектах, чтобы модель могла сгенерировать более развернутый текст.'''
)

# Запрос к GigaChat с использованием определенных сообщений
response = giga([system_message, human_message])

# Вывод результата
print(response.content)
