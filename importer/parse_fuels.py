import json

import googletrans
from bs4 import BeautifulSoup

if __name__ == '__main__':
    translator = googletrans.Translator()
    options = {}
    with open('fuels.txt', 'r', encoding='utf8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        inputs = soup.find_all('option')
        options = []
        for input in inputs:
            print(input)
            code = input.attrs['value']
            name = input.text
            translated = translator.translate(name, src='ko', dest='ru')
            text = translated.text
            options.append({
                'name': name,
                'code': code,
                'label': text,
            })
        print(options)
    with open('translated_fuels.json', 'w', encoding='utf8') as file:
        file.write(json.dumps(options))
