import json

import googletrans
from bs4 import BeautifulSoup

if __name__ == '__main__':
    translator = googletrans.Translator()
    options = {}
    with open('kia_models.txt', 'r', encoding='utf8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        inputs = soup.find_all('li')
        options = []
        for input in inputs:
            print(input)
            code = input.attrs['data-no']
            name = input.text
            translated = translator.translate(name, src='ko', dest='en')
            text = translated.text
            options.append({
                'name': name,
                'code': code,
                'label': text,
            })
        print(options)
    with open('translated_kia.json', 'w', encoding='utf8') as file:
        file.write(json.dumps(options))
