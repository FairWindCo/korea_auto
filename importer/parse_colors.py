import json

import googletrans
from bs4 import BeautifulSoup

if __name__ == '__main__':
    translator = googletrans.Translator()
    options = {}
    with open('colors.txt', 'r', encoding='utf8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        inputs = soup.find_all('option')
        options = []
        for input in inputs:
            print(input)
            code = input.attrs['value']
            name = input.text
            translated = translator.translate(name, src='ko', dest='en')
            text_en = translated.text
            text_ru = translator.translate(text_en, src='en', dest='ru').text
            options.append({
                'name': name,
                'code': code,
                'label': f'{text_ru} ({text_en})',
            })
        print(options)
    with open('translated_colors.json', 'w', encoding='utf8') as file:
        file.write(json.dumps(options))
