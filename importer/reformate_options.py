import json

import googletrans
from bs4 import BeautifulSoup

if __name__ == '__main__':
    translator = googletrans.Translator()
    options = {}
    with open('options_template.txt', 'r', encoding='utf8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        inputs = soup.find_all('input', attrs={
            'type':'checkbox'
        })

        for input in inputs:
            print(input)
            key = input.attrs['id']
            if 'value' in input.attrs:
                value = input.attrs['value']
                options[key] = {
                    'name': '',
                    'code': value
                }
        labels = soup.find_all('label')
        for label in labels:
            key = label.attrs['for']
            if key in options:
                options[key]['name'] = label.text
                try:
                    translated = translator.translate(label.text, src='ko', dest='ru')
                    options[key]['label'] = translated.text
                    print(options[key]['label'])
                except Exception as e:
                    print(e)
        print(options)
    with open('translated.json', 'w', encoding='utf8') as file:
        file.write(json.dumps(options))