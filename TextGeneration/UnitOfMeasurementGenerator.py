from decouple import config
from gigachat.exceptions import AuthenticationError
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

class UnitOfMeasurementGenerator:
    def __init__(self):
        self._initialize_gigachat()

    def _initialize_gigachat(self):
        self.auth = config('auth', default='')
        self.giga = GigaChat(credentials=self.auth,
                             model='GigaChat:latest',
                             verify_ssl_certs=False)

    def normalize_unit(self, unit):
        unit_mapping = {
            'грамм': 'г (GRM)',
            'г': 'г (GRM)',
            'килограмм': 'кг (KGM)',
            'кг': 'кг (KGM)',
            'литр': 'л (дм3) (LTR)',
            'литры': 'л (дм3) (LTR)',
            'л': 'л (дм3) (LTR)',
            'метр': 'м (MTR)',
            'м': 'м (MTR)',
            'квадратный метр': 'м2',
            'м2': 'м2',
            'кубический метр': 'м3 (MTQ)',
            'м3': 'м3 (MTQ)',
            'миллиграмм': 'мг (MGM)',
            'мг': 'мг (MGM)',
            'миллилитр': 'мл.',
            'мл': 'мл.',
            'набор': 'набор (SET)',
            'шт': 'шт (PCE)',
            'штука': 'шт (PCE)',
            'штуки': 'шт (PCE)',
            # добавьте другие преобразования, если необходимо
        }
        return unit_mapping.get(unit.lower(), 'Неопределено')

    def generate_units_of_measurement(self, product_names):
        system_message = SystemMessage(
            content='''Ты - опытный специалист по номенклатуре и единицам измерения.
            Твоя задача - определить единицу измерения для каждой номенклатуры.
            Укажи единицу измерения для каждой номенклатуры, используя международное сокращение, если оно существует.'''
        )

        valid_units = {
            '%', '1000 руб', 'г (GRM)', 'кар (CTM)', 'кВт.ч (KWH)', 'кг (KGM)',
            'км/1000 м (KMT)', 'компл', 'кор', 'л (дм3) (LTR)', 'м (MTR)',
            'м2', 'м2 (MTK)', 'м3 (MTQ)', 'мг (MGM)', 'мл.', 'набор (SET)',
            'пак', 'пал', 'пар (NPR)', 'пач', 'руб', 'см3 (мл) (CMQ)', 'т (TNE)',
            'упак (NMP)', 'ч (HUR)', 'шт (PCE)', 'ящ'
        }

        units_of_measurement = []
        for product_name in product_names:
            human_message = HumanMessage(
                content=f'''Название товара: {product_name}.
                Укажи единицу измерения для этой номенклатуры. Верни только ЕДИНИЦУ ИЗМЕРЕНИЯ И НИЧЕГО БОЛЕЕ, используя международное сокращение, если оно существует.'''
            )
            try:
                response = self.giga([system_message, human_message])
            except AuthenticationError:
                self._initialize_gigachat()  # Переинициализация GigaChat с новыми учетными данными
                response = self.giga([system_message, human_message])

            unit = response.content.strip()
            # print(f"Ответ модели: {unit}")  # Отладочная информация
            normalized_unit = self.normalize_unit(unit)
            if normalized_unit in valid_units:
                units_of_measurement.append(normalized_unit)
            else:
                units_of_measurement.append('Неопределено')

        return units_of_measurement

# Пример использования
# generator = UnitOfMeasurementGenerator()
# product_names = ["Вода", "Мука", "Молоко", 'подшибники', 'Коферка BOSTON']
# units_of_measurement = generator.generate_units_of_measurement(product_names)
# for unit in units_of_measurement:
#     print(unit)
