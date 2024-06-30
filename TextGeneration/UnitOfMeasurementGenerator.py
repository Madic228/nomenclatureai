from decouple import config
from gigachat.exceptions import AuthenticationError
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.chat_models.gigachat import GigaChat

class UnitOfMeasurementGenerator:
    def __init__(self):
        self._initialize_gigachat()

    def _initialize_gigachat(self):
        # self.auth = config('AUTH', default='')
        self.auth = "NTdlOGY2NWEtODY5OS00M2I3LWE3MmEtMGQyNzQ5MDEzNThhOmI4MjZhMzZmLWIwMDEtNDkzYi05MzhkLTZmMmZlOGY1YTYwZA=="
        self.giga = GigaChat(credentials=self.auth,
                             model='GigaChat:latest',
                             verify_ssl_certs=False)

    def normalize_unit(self, unit):
        unit_mapping = {
            '%': '%',
            '1000 руб': '1000 руб',
            'грамм': 'г (GRM)',
            'граммы': 'г (GRM)',
            'г': 'г (GRM)',
            'гр': 'г (GRM)',
            'килограмм': 'кг (KGM)',
            'килограммы': 'кг (KGM)',
            'кг': 'кг (KGM)',
            'литр': 'л (дм3) (LTR)',
            'литры': 'л (дм3) (LTR)',
            'л': 'л (дм3) (LTR)',
            'л.': 'л (дм3) (LTR)',
            'литра': 'л (дм3) (LTR)',
            'метр': 'м (MTR)',
            'метры': 'м (MTR)',
            'м': 'м (MTR)',
            'м.': 'м (MTR)',
            'квадратный метр': 'м2',
            'квадратные метры': 'м2',
            'м2': 'м2',
            'м^2': 'м2',
            'кубический метр': 'м3 (MTQ)',
            'кубические метры': 'м3 (MTQ)',
            'м3': 'м3 (MTQ)',
            'м^3': 'м3 (MTQ)',
            'миллиграмм': 'мг (MGM)',
            'миллиграммы': 'мг (MGM)',
            'мг': 'мг (MGM)',
            'мг.': 'мг (MGM)',
            'миллилитр': 'мл.',
            'миллилитры': 'мл.',
            'мл': 'мл.',
            'мл.': 'мл.',
            'набор': 'набор (SET)',
            'наборы': 'набор (SET)',
            'шт': 'шт (PCE)',
            'шт.': 'шт (PCE)',
            'штука': 'шт (PCE)',
            'штуки': 'шт (PCE)',
            'штук': 'шт (PCE)',
            'пара': 'пар (NPR)',
            'пары': 'пар (NPR)',
            'пар': 'пар (NPR)',
            'ящики': 'ящ',
            'ящик': 'ящ',
            'ящика': 'ящ',
            'ящиков': 'ящ',
            'кар': 'кар (CTM)',
            'карат': 'кар (CTM)',
            'метрический карат': 'кар (CTM)',
            'кВт.ч': 'кВт.ч (KWH)',
            'киловатт-час': 'кВт.ч (KWH)',
            'киловатт-часы': 'кВт.ч (KWH)',
            'кВт': 'кВт.ч (KWH)',
            'кВт.': 'кВт.ч (KWH)',
            'километр': 'км/1000 м (KMT)',
            'километры': 'км/1000 м (KMT)',
            'км': 'км/1000 м (KMT)',
            'км.': 'км/1000 м (KMT)',
            'комплект': 'компл',
            'комплекты': 'компл',
            'компл': 'компл',
            'коробка': 'кор',
            'коробки': 'кор',
            'кор': 'кор',
            'пакет': 'пак',
            'пакеты': 'пак',
            'пак': 'пак',
            'палета': 'пал',
            'палеты': 'пал',
            'пал': 'пал',
            'пачка': 'пач',
            'пачки': 'пач',
            'пач': 'пач',
            'рубль': 'руб',
            'рубли': 'руб',
            'руб': 'руб',
            'кубический сантиметр': 'см3 (мл) (CMQ)',
            'кубические сантиметры': 'см3 (мл) (CMQ)',
            'см3': 'см3 (мл) (CMQ)',
            'см^3': 'см3 (мл) (CMQ)',
            'тонна': 'т (TNE)',
            'тонны': 'т (TNE)',
            'т': 'т (TNE)',
            'упаковка': 'упак (NMP)',
            'упаковки': 'упак (NMP)',
            'упак': 'упак (NMP)',
            'уп': 'упак (NMP)',
            'уп.': 'упак (NMP)',
            'час': 'ч (HUR)',
            'часы': 'ч (HUR)',
            'ч': 'ч (HUR)',
            'ч.': 'ч (HUR)',

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
                Укажи единицу измерения для этой номенклатуры. Верни только ЕДИНИЦУ ИЗМЕРЕНИЯ И НИЧЕГО БОЛЕЕ, используя международное сокращение, если оно существует. P.S. парные предметы измеряются в парах.'''
            )
            try:
                response = self.giga([system_message, human_message])
            except AuthenticationError:
                self._initialize_gigachat()  # Переинициализация GigaChat с новыми учетными данными
                response = self.giga([system_message, human_message])

            unit = response.content.strip()
            print(f"Ответ модели: {unit}")  # Отладочная информация
            normalized_unit = self.normalize_unit(unit)
            if normalized_unit in valid_units:
                units_of_measurement.append(normalized_unit)
            else:
                units_of_measurement.append('Неопределено')

        return units_of_measurement

# Пример использования
generator = UnitOfMeasurementGenerator()
product_names = [
    'Молоко',
    'Сахар',
    'Шоколад',
    'Масло подсолнечное',
    'Яблоки',
    'Кофе растворимый',
    'Пачка чая',
    'Пакет молока',
    'Мука',
    'Томатная паста',
    'Сыр',
    'Картофель',
    'Банка консервов',
    'Пачка макарон',
    'Сметана',
    'Куриные яйца',
    'Тетрадь',
    'Носки',
    'Коробка конфет',
    'Шампунь',
    'Мыло',
    'Стиральный порошок'
]
units_of_measurement = generator.generate_units_of_measurement(product_names)
for unit in units_of_measurement:
    print(unit)
