# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
import json
import os
import re
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


def base64_ecoder(text):
    message_bytes = text.encode('utf8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf8')
    return base64_message


def convert_password(password):
    quoted = quote(password)
    return base64_ecoder(quoted)


def login2(user, password):
    session = requests.Session()
    url = 'http://www.carmanager.co.kr/User/Login/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml;     q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;     v = b3;  q = 0.9',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    }
    resp = session.get(url, headers=header)
    soup = BeautifulSoup(resp.content, 'html.parser')
    cookies = resp.cookies
    # print(resp.text)

    elements = soup.find_all('ul', class_='login-input')

    if elements:
        print('NEED LOGIN')
        url = 'http://www.carmanager.co.kr/User/Login'
        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        resp = session.post(url, data={
            'cbxrememberid': 'on',
            'sbxgubun': '1',
            'returnurl': '',
            'userid': user,
            'userpwd': password
        }, cookies=cookies, headers=header)
        soup = BeautifulSoup(resp.content, 'html.parser')
        elements = soup.find_all('ul', class_='login-input')
        menu_div = soup.find('div', id='ui_logingnb')
        menu_element = menu_div.find('a', attrs={'href': '/User/Logout'})
        if not elements and menu_div and menu_element:
            print(menu_element)
            print('LOGIN - OK!')
            print('COOKIES ', session.cookies.get_dict())
            url = 'http://www.carmanager.co.kr/'
            resp = session.get(url, headers=header)
            if test_page_is_login(resp.content):
                print('MAIN PAGE')
                url = 'http://www.carmanager.co.kr/Car/Data'
                resp = session.get(url, headers=header)
                if test_page_is_login(resp.content):
                    return True, session
                else:
                    return False, 'NO LOGIN ON CAR DATA PAGE'
            else:
                return False, 'NO LOGIN ERROR'
        else:
            print('Этот идентификатор не существует.')
            print(resp.text)
            return False, 'Этот идентификатор не существует.'
    else:
        print(resp.text)
        return False, 'Шаблон сайта не совпадает'


def get_page_data(session, page=1, per_page_count=10, region=103, area=1035, donji=94001, brand=None, model=None):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange; v = b3;  q = 0.9',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    }
    url = 'http://www.carmanager.co.kr/CarData/JsonCarData'
    page_param = {
        "PageNow": page,
        "PageSize": per_page_count,
        "PageSort": "0",
        "PageAscDesc": "1",
        "CarMode": "0",
        "CarSiDoNo": region,  # Убрать регион
        "CarSiDoAreaNo": area,  # Убрать регион
        "CarDanjiNo": donji,  # Убрать регион
        "CarMakerNo": brand,  # 10056 - KIA 10055 - HYNDAI
        "CarModelNo": model,  # номер модели
        "CarModelDetailNo": "",  # версия модели (новая, страя и т.п.)
        "CarGradeNo": "",  # код версии c учетом оьъема и кузова
        "CarGradeDetailNo": "",
        "CarMakeSDate": "",  # 2015-01 год и месяц начала поиска дата изготовления машины
        "CarMakeEDate": "",  # 2015-01 год и месяц конца поиска
        "CarDriveSKm": None,  # вероятно диапазон пробега
        "CarDriveEKm": None,
        "CarMission": "",
        "CarFuel": "",
        "CarColor": "",
        "CarSMoney": None,
        "CarEMoney": None,
        "CarIsLPG": "False",
        "CarIsSago": "False",
        "CarIsPhoto": "False",
        "CarIsSaleAmount": "False",
        "CarIsCarCheck": "False",
        "CarName": "",
        "CarDealerName": "",
        "CarShopName": "",
        "CarDealerHP": "",
        "CarNumber": "",
        "CarOption": "",  # Опции
        "CarTruckTonS": "",
        "CarTruckTonE": ""
    }
    resp = session.post(url, data=page_param, headers=header)
    return resp.json()


def test_page_is_login(page):
    soup = BeautifulSoup(page, 'html.parser')
    elements = soup.find_all('ul', class_='login-input')
    menu_div = soup.find('div', id='ui_logingnb')
    menu_element = menu_div.find('a', attrs={'href': '/User/Logout'})
    print(elements, menu_element)
    return True if not elements and menu_element else False


def login(user, password):
    url = 'https://www.glovisaa.com/login.do'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml;     q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;     v = b3;  q = 0.9',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    }
    resp = requests.get(url, headers=header)

    soup = BeautifulSoup(resp.content, 'html.parser')
    cookies = resp.cookies
    # print(resp.text)

    elements = soup.find_all('div', class_='logincon')

    if elements:
        print('NEED LOGIN')
        url = 'https://www.glovisaa.com/loginProc.do'
        # passno: a29yZXgwNTIwJTQw
        # idsaveyn: N
        # id: 9505
        # returnUrl:
        header['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        d = {
            'passno': convert_password(password),
            'idsaveyn': 'N',
            'id': user,
            'returnUrl': '',
        }
        print(d)
        resp = requests.post(url, data=d, cookies=cookies, headers=header)
        result_obj = resp.json()
        if result_obj:
            cookies = resp.cookies
            print('TEST')
            print(resp.request.headers)
            print(resp.request.body)
            print(resp.json())
            url = 'https://www.glovisaa.com/main.do'
            resp = requests.get(url, cookies=cookies, headers=header)
            # 'https://www.glovisaa.com/memcompany/memAuctionList.do'
            print(resp.text)
        else:
            print('Этот идентификатор не существует.')
            print(resp.text)
    else:
        print(resp.text)



def get_and_write_file(url, path, name, session):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    }
    r = session.get(url, headers=header)
    if r.status_code == 200:
        with open(f'{path}/{name}', 'wb') as file:
            file.write(r.content)
        print(f'WRITE {url} to FILE {path}/{name}')
        return r.content
    else:
        print(f'WRITE ERROR {r.status_code} IN {url}')
        return None


reg_exp = re.compile(r'[0-9]+')
reg_exp_url = re.compile((r'url\([A-Za-z0-9\/\.-_]+\)'))


def process_protocol(code, path, session):
    content = get_and_write_file(f'http://autocafe.co.kr/ASSO/CarCheck_Form.asp?OnCarNo={code}', path, 'add.html', session)
    soap = BeautifulSoup(content, 'html.parser')
    protocol_image = 1
    url_replaced = {}
    images = soap.find_all('img')
    for image in images:
        url_img = image.attrs['src']
        if not url_img in url_replaced:
            key = url_img
            if not url_img.startswith('http'):
                url_img = 'http://autocafe.co.kr/ASSO/' + url_img
            image_file = f'protocol_img_{protocol_image}.jpg'
            res = get_and_write_file(url_img, path, image_file, session)
            if res:
                url_replaced[key] = image_file
                image.attrs['src'] = image_file
                protocol_image += 1
        else:
            image.attrs['src'] = url_replaced[url_img]
    tables = soap.find_all('table', attrs={
        'title': '자동차 종합상태'
    })
    for table in tables:
        divs = table.find_all('div')
        for div in divs:
            if 'style' in div.attrs and div.attrs['style'].find('background-image:url'):
                val = reg_exp_url.findall(div.attrs['style'])
                if val:
                    url_img = val[0][4:-1]
                    if not url_img in url_replaced:
                        key = url_img
                        if not url_img.startswith('http'):
                            url_img = 'http://autocafe.co.kr/ASSO/' + url_img
                        image_file = f'protocol_img_{protocol_image}.jpg'
                        res = get_and_write_file(url_img, path, image_file, session)
                        if res:
                            url_replaced[key] = image_file
                            div.attrs['style'] = reg_exp_url.sub(f"url({image_file})", div.attrs['style'])
                            protocol_image += 1
                    else:
                        div.attrs['style'] = reg_exp_url.sub(f"url({url_replaced[url_img]})", div.attrs['style'])
    with open(f'{path}/add.html', "wb") as f_output:
        f_output.write(soap.prettify("utf-8"))


def process_additional_data(content, session, path):
    soap = BeautifulSoup(content, 'html.parser')
    images = soap.find_all('img')
    image_count = 1
    for image in images:
        if 'alt' not in image.attrs and (
                'onerror' in image.attrs or ('style' in image.attrs and image.attrs['style'] == 'display:none;')):
            get_and_write_file(image.attrs['src'], path, f'big_image_{image_count}.jpg', session)
            image_count = image_count + 1
    maps = soap.find_all('map', attrs={'name': 'carPoint'})
    for el in maps:
        areas = el.find_all('area')
        for area in areas:
            if 'onclick' in area.attrs:
                print(area.attrs['onclick'])
                val = reg_exp.findall(area.attrs['onclick'])
                if val:
                    process_protocol(val[0], path, session)


def process_car_data(object_car, path, session):
    carno = object_car['CarNo']
    car_path = f'{path}/{carno}'
    if not os.path.exists(car_path):
        os.mkdir(car_path)
        with open(f'{car_path}/car_data.json', 'w') as file:
            file.write(json.dumps(object_car))
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Accept': 'text / html, application / xhtml + xml, application / xml;     q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;     v = b3;  q = 0.9',
            'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
        }
        image_thb = object_car['CarImageThumb']
        if image_thb:
            get_and_write_file(image_thb, car_path, f'ImageThumb.jpg', session)
        url = f'http://www.carmanager.co.kr/PopupFrame/CarDetail/{carno}'
        data = get_and_write_file(url, car_path, f'detail.html', session)
        if data:
            process_additional_data(data, session, car_path)
        for i in range(1, 6):
            key_name = f'CarMarkImageURL{i}'
            image_url = object_car[key_name]
            if image_url:
                get_and_write_file(f'http://www.carmanager.co.kr/{image_url}', car_path, f'image_{i}.gif', session)


def import_car_data(login, password, db_path='DataBase', max_page=1, per_page_count=10, region=103, area=1035,
                    donji=94001,
                    brand=None, model=None):
    res, info = login2(login, password)
    if res:
        session = info
        objects = get_page_data(session, 1, per_page_count, region, area, donji, brand, model)
        total_count = objects[0]['CountTotal']
        print(f'TOTAL CARS ON SITE WITH REQUEST PARAMS {total_count}')
        for obj in objects:
            process_car_data(obj, db_path, session)
        for i in range(2, max_page):
            objects = get_page_data(session, i)
            for obj in objects:
                for obj in objects:
                    process_car_data(obj, db_path, session)
    else:
        print(info)
