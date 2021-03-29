import glob
import os
import re

from bs4 import BeautifulSoup, NavigableString
from django.utils.datetime_safe import datetime

from importer.translate_report import translate_report_content

simple_year_reg_expr = re.compile('(&nbsp;)*\s*(\(3\)|③)(&nbsp;)*\s*(Год производства|Год выпуска|연식)\s*(&nbsp;)*')
year_value_reg_expr = re.compile(r'\s*19|20[0-9]{2}\s*')
simple_vin_reg_expr = re.compile('(&nbsp;)*\s*(\(6\)|⑥)(&nbsp;)*\s*(VIN|차대번호).*?')
vin_value_reg_expr = re.compile(r'\s*([A-Z0-9]{15,20})\s*')
simple_drive_reg_expr = re.compile('(&nbsp;)*\s*(\(9\)|⑨)(&nbsp;)*\s*(Двигатель|원동기형식).*?')
drive_value_reg_expr = re.compile(r'\s*([A-Z0-9\- ]{3,12})\s*')
# (5) Дата первоначальной регистрации
simple_reg_date_reg_expr = re.compile('(&nbsp;)*\s*(\(5\)|⑤)(&nbsp;)*\s*(Дата первоначальной регистрации|최초등록일).*?')
reg_date_value_reg_expr = re.compile(r'\s*19|20[0-9]{2}\s*[\.\-/\\]\s*[0-9]{2}\s*[\.\-/\\]\s*[0-9]{2}\s*')


def neighbour_data_extractor(soup, pattern, data_pattern):
    data = None
    result = soup.find_all(text=pattern)
    if not result:
        result = soup.find_all(string=pattern)
    if result:
        if isinstance(result[0], NavigableString):
            tag = result[0].parent
        else:
            tag = result[0]
        count = 0
        parent_tag = tag
        while parent_tag.name != 'tr':
            parent_tag = parent_tag.parent
            count += 1
            if count > 3:
                parent_tag = None
                break
        if parent_tag:
            current_find = False
            for sub_tag in parent_tag.findAll():
                if current_find:
                    if sub_tag.contents and len(sub_tag.contents) > 1:
                        finde_tag = sub_tag.find(text=data_pattern)
                        if finde_tag:
                            data = finde_tag.string.strip()
                        else:
                            finde_tag = sub_tag.find(string=data_pattern)
                            if finde_tag:
                                data = finde_tag.string.strip()
                            else:
                                if data_pattern.match(sub_tag.text):
                                    data = sub_tag.text.strip()
                                else:
                                    print(sub_tag.text.strip())
                    else:
                        data = sub_tag.string.strip()
                    break
                if sub_tag == tag:
                    current_find = True
    return data


def extractor(content):
    soup = BeautifulSoup(content, 'html.parser')
    year = neighbour_data_extractor(soup, simple_year_reg_expr, year_value_reg_expr)
    vin = neighbour_data_extractor(soup, simple_vin_reg_expr, vin_value_reg_expr)
    drive = neighbour_data_extractor(soup, simple_drive_reg_expr, drive_value_reg_expr)
    red_date = neighbour_data_extractor(soup, simple_reg_date_reg_expr, reg_date_value_reg_expr)

    if year:
        try:
            year = int(year)
        except ValueError:
            year = None

    if red_date:
        date_str = re.sub(r'[\\ \.\-\/]+', '-', red_date)
        try:
            red_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            red_date = None

    result = (year, vin, drive, red_date)

    return result


def process_report_file(path, dir, translator, can_save=True, replace_standart=True):
    file_path = os.path.abspath(os.path.join(path, dir, 'add.html'))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                content = file.read()
                year, vin, drive, red_date = extractor(content)
            if can_save:
                with open(file_path, "w", encoding='utf8') as f_output:
                    translated_content = translate_report_content(content)
                    print(content)
                    f_output.write(translated_content)
            return vin, red_date, year, drive
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
