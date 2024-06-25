from TextGeneration.ProductDescriptionGenerator import ProductDescriptionGenerator

generator = ProductDescriptionGenerator()
product_names = ["Пылесос мобиль ", "Соковыжималка МАЛО"] # Можно передать несколько товаров/номенклатур
keywords = ['Надежность', 'качество'] # Не обязательное поле Ключевые слова
descriptions = generator.generate_description(product_names, keywords=keywords)
for description in descriptions:
    print(description)