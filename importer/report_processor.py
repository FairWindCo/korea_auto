import glob
import os
from datetime import datetime

from bs4 import BeautifulSoup, NavigableString


def process_year_creation(records, start_index, max_index):
    year = None
    while start_index < max_index:
        elements = records[start_index].find_all()
        if elements[0].text.strip() == '(3) 연식':
            elements[0].string = '(3) Год производства'
            year = elements[1].text.strip()
            break
        elif elements[0].text.strip() == '(3) Год производства':
            year = elements[1].text.strip()
            break
        start_index += 1
    return start_index + 1, year


def process_vin_code(records, start_index, max_index):
    vin = None
    while start_index < max_index:
        elements = records[start_index].find_all()
        if elements[0].text.strip() == '(6) 차대번호':
            elements[0].string = '(6) VIN Код'
            vin = elements[1].text.strip()
            break
        elif elements[0].text.strip() == '(6) VIN Код':
            vin = elements[1].text.strip()
            break
        start_index += 1
    return start_index + 1, vin


def process_fuel(records, start_index, max_index):
    vin = None
    while start_index < max_index:
        elements = records[start_index].find_all()
        if elements[0].text.strip() == '(8) 사용연료':
            elements[0].string = '(8) Тип топлива'
            sub_elements = elements[1].find_all(text=True)
            sub_elements[1].replace_with(NavigableString('Бензин'))
            sub_elements[2].replace_with(NavigableString('Дизель'))
            sub_elements[3].replace_with(NavigableString('Газ (LPG)'))
            sub_elements[4].replace_with(NavigableString('Гибридный'))
            sub_elements[5].replace_with(NavigableString('Электро'))
            sub_elements[6].replace_with(NavigableString('Водород'))
            sub_elements[7].replace_with(NavigableString('Другой'))
            break
        elif elements[0].text.strip() == '(8) Тип топлива':
            break
        start_index += 1
    return start_index + 1


def process_first(records, start_index, max_index):
    while start_index < max_index:
        elements = records[start_index].find_all()
        if elements[0].text.strip() == '(1) 차명':
            elements[0].string = '(1) Модель'
            if elements[3].text.strip() == '(2)자동차등록번호':
                elements[3].string = '(2) Регистрационный номер'
        elif elements[0].text.strip() == '(1) Модель':
            break
        start_index += 1
    return start_index + 1


def process_drive(records, start_index, max_index):
    drive = None
    while start_index < max_index:
        elements = records[start_index].find_all()
        if elements[0].text.strip() == '(9) 원동기형식':
            elements[0].string = '(9) Двигатель'
            drive = elements[1].text.strip()
            if elements[2].text.strip() == '(10) 보증유형':
                elements[2].string = '(10) Тип гарантии'
                sub_elements = elements[3].find_all(text=True)

                sub_elements[1].replace_with(NavigableString('Самостоятельная гарантия'))
                sub_elements[2].replace_with(NavigableString('Гарантия страховой компании'))
            if elements[6].text.strip() == '가격산정 기준가격':
                elements[6].string = 'База для расчета цены'
            if elements[8].text.strip() == '만원':
                elements[8].string = 'Десять тысяч вон'
            break
        elif elements[0].text.strip() == '(9) Двигатель':
            drive = elements[1].text.strip()
            break
        start_index += 1
    return start_index + 1, drive


def process_first_registration(records, start_index, max_index):
    reg_date = None
    while start_index < max_index:
        elements = records[start_index].find_all()
        if elements[0].text.strip() == '(5) 최초등록일':
            elements[0].string = '(5) Дата первоначальной регистрации'
            reg_date = elements[1].text.strip()
            if elements[2].text.strip() == '(7) 변속기':
                elements[2].string = '(7) Трансмиссия'
                sub_elements = elements[3].find_all(text=True)

                sub_elements[1].replace_with(NavigableString('Автоматическая'))
                sub_elements[2].replace_with(NavigableString('Ручная'))
                sub_elements[3].replace_with(NavigableString('Полуавтоматическая'))
                sub_elements[4].replace_with(NavigableString('Бесступенчатая трансмиссия'))
                sub_elements[5].replace_with(NavigableString('Другое ()'))
            break
        elif elements[0].text.strip() == '(5) Дата первоначальной регистрации':
            reg_date = elements[1].text.strip()
            break
        start_index += 1
    return start_index + 1, reg_date


def process_report_file(path, dir, translator, can_save=True, replace_standart=True):
    file_path = os.path.abspath(os.path.join(path, dir, 'add.html'))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                content = file.read()
            if replace_standart:
                replacer = {
                    '만원': ' дес. тыс. Вон',
                    '없음': 'Нет',
                    '있음': 'Есть',
                    '양호': 'Хорошо',
                    '불량': 'Плохо',
                    '미세누유': 'Микропротекание',
                    '누유': 'Утечка',
                    '적정': 'Адекватно',
                    '부족': 'Мало',
                    '과다': 'Много',

                }
                for key, val in replacer.items():
                    content = content.replace(key, val)
                    # content = content.replace('만원', ' дес. тыс. Вон').replace('없음', 'Нет').replace('있음', 'Есть')
            soup = BeautifulSoup(content, 'html.parser')
            records = soup.find_all('tr')
            index = 0
            table_1 = soup.find('table', attrs={
                'title': '자동차 기본정보'
            })
            if table_1:
                records = table_1.find_all('tr')
                size = len(records)
                index = process_first(records, 0, size)
                index, year = process_year_creation(records, index, size)
                index, reg_date = process_first_registration(records, index, size)
                index, vin = process_vin_code(records, index, size)
                index = process_fuel(records, index, size)
                index, drive = process_drive(records, index, size)

                if can_save:
                    with open(file_path, "wb") as f_output:
                        f_output.write(soup.prettify("utf-8"))

                return vin, datetime.strptime(reg_date.strip().replace('.', '-'), '%Y-%m-%d'), int(year), drive
        except Exception as e:
            print(f'ERROR in add.html dir {dir} {e}')
    else:
        print(f'ERROR NO FILE add.html in {dir}')
    return None, None, None, None


def get_images_counts(path, dir):
    file_path_1 = os.path.abspath(os.path.join(path, dir, 'big_image_*.jpg'))
    file_path_2 = os.path.abspath(os.path.join(path, dir, 'image_*.gif'))
    big_images = glob.glob(file_path_1)
    small_images = glob.glob(file_path_2)
    return len(big_images), len(small_images)
