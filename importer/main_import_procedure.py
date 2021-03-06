# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import base64
import json
import os
import random
import re
from urllib.parse import quote, urlparse

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError

from korea_auto import settings


def base64_ecoder(text):
    message_bytes = text.encode('utf8')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('utf8')
    return base64_message


def convert_password(password):
    quoted = quote(password)
    return base64_ecoder(quoted)


def login2(user, password, proxy=None, timeout=5):
    session = requests.Session()
    url = 'http://www.carmanager.co.kr/User/Login/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml;     q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;     v = b3;  q = 0.9',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    }

    resp = session.get(url, headers=header, proxies=proxy)
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
        }, cookies=cookies, headers=header, proxies=proxy, timeout=timeout)
        soup = BeautifulSoup(resp.content, 'html.parser')
        elements = soup.find_all('ul', class_='login-input')
        menu_div = soup.find('div', id='ui_logingnb')
        menu_element = menu_div.find('a', attrs={'href': '/User/Logout'})
        if not elements and menu_div and menu_element:
            print(menu_element)
            print('LOGIN - OK!')
            print('COOKIES ', session.cookies.get_dict())
            url = 'http://www.carmanager.co.kr/'
            resp = session.get(url, cookies=cookies, headers=header, proxies=proxy, timeout=timeout)
            if test_page_is_login(resp.content):
                print('MAIN PAGE')
                url = 'http://www.carmanager.co.kr/Car/Data'
                resp = session.get(url, cookies=cookies, headers=header, proxies=proxy)
                if test_page_is_login(resp.content):
                    return True, session
                else:
                    return False, 'NO LOGIN ON CAR DATA PAGE'
            else:
                return False, 'NO LOGIN ERROR'
        else:
            print('???????? ?????????????????????????? ???? ????????????????????.')
            print(resp.text)
            return False, '???????? ?????????????????????????? ???? ????????????????????.'
    else:
        print(resp.text)
        return False, '???????????? ?????????? ???? ??????????????????'


def get_page_data(session, page=1, per_page_count=10, region=103, area=1035, donji=94001, brand=None, model=None,
                  proxy=None, timeout=5):
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
        # "CarSiDoNo": region,  # ???????????? ????????????
        # "CarSiDoAreaNo": area,  # ???????????? ????????????
        # "CarDanjiNo": donji,  # ???????????? ????????????
        "CarMakerNo": brand,  # 10056 - KIA 10055 - HYNDAI
        "CarModelNo": model,  # ?????????? ????????????
        "CarModelDetailNo": "",  # ???????????? ???????????? (??????????, ?????????? ?? ??.??.)
        "CarGradeNo": "",  # ?????? ???????????? c ???????????? ???????????? ?? ????????????
        "CarGradeDetailNo": "",
        "CarMakeSDate": "",  # 2015-01 ?????? ?? ?????????? ???????????? ???????????? ???????? ???????????????????????? ????????????
        "CarMakeEDate": "",  # 2015-01 ?????? ?? ?????????? ?????????? ????????????
        "CarDriveSKm": None,  # ???????????????? ???????????????? ??????????????
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
        "CarOption": "",  # ??????????
        "CarTruckTonS": "",
        "CarTruckTonE": ""
    }
    if region and region >= 0 and region != ['-']:
        page_param["CarSiDoNo"] = region
    if area and area >= 0 and area != '-':
        page_param["CarSiDoAreaNo"] = area
    if donji and donji >= 0 and donji != '-':
        page_param["CarDanjiNo"] = donji
    resp = session.post(url, data=page_param, headers=header, proxies=proxy, timeout=timeout)
    return resp.json()


def test_page_is_login(page):
    soup = BeautifulSoup(page, 'html.parser')
    elements = soup.find_all('ul', class_='login-input')
    menu_div = soup.find('div', id='ui_logingnb')
    menu_element = menu_div.find('a', attrs={'href': '/User/Logout'})
    print(elements, menu_element)
    return True if not elements and menu_element else False


def login(user, password, proxy=None):
    url = 'https://www.glovisaa.com/login.do'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text / html, application / xhtml + xml, application / xml;     q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;     v = b3;  q = 0.9',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    }
    params = {
        'header': header
    }

    resp = requests.get(url, headers=header, proxies=proxy)
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
            print('???????? ?????????????????????????? ???? ????????????????????.')
            print(resp.text)
    else:
        print(resp.text)


def get_and_write_file_cached(cache, index, url, path, name, session, save_original_name=False, add_name_part='img',
                              base_site_url='', return_content_cached=False,
                              proxy=None, timeout=5):
    if not url:
        return False, url

    if url[0] == '.' and url[1] == '/':
        url = url[1:]
    if url not in cache:
        content, file_name = get_and_write_file(url, path, f'{index}{name}', session, save_original_name, add_name_part,
                                                base_site_url, proxy=proxy, timeout=timeout)
        cache[url] = file_name
        return content, file_name
    else:
        file_name = cache[url]
        if return_content_cached:
            file_path = os.path.join(path, file_name)
            try:
                with open(file_path, 'rb') as file:
                    content = file.read()
                return content, file_name
            except Exception as e:
                print(f'READ FILE {file_path} EXCEPTION: {e}')
                return None, file_name
        else:
            return True, file_name


def get_and_write_file(url, path, name, session, save_original_name=False, add_name_part='img', base_site_url='',
                       proxy=None, timeout=5):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
        'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    }
    params = {
        'headers': header
    }
    if not url.startswith('http'):
        file_url = base_site_url + url
    else:
        file_url = url
    try:
        r = session.get(file_url, headers=header, proxies=proxy, timeout=timeout)
    except ConnectionError:
        r = None
    except ProxyError:
        r = None
    if r and r.status_code == 200:
        if save_original_name:
            url_elements = urlparse(file_url)
            if url_elements:
                file_part = os.path.basename(url_elements.path)
                file_name = f'{add_name_part}_{file_part}'
            else:
                file_name = f'{add_name_part}_{name}'
            file_path = os.path.join(path, file_name)
            if os.path.exists(file_path):
                file_name = f'{file_name}_{random.randint(0, 50)}_{random.randint(0, 50)}_{random.randint(0, 50)}'
        else:
            file_name = f'{add_name_part}_{name}' if add_name_part else name
        file_path = os.path.join(path, file_name)
        try:
            with open(file_path, 'wb') as file:
                file.write(r.content)
            print(f'WRITE URL="{url}" to FILE "{file_path}"')
            return r.content, file_name
        except Exception as e:
            print(f'WRITE ERROR: {e} FOR URL "{url}"  PROXY={proxy}')
            return None, file_name
    else:
        if r is None:
            print(f'GET ERROR FOR URL "{url}" PROXY={proxy}')
            return None, None
        print(f'GET ERROR: {r.status_code} FOR URL "{url}"  PROXY={proxy}')
        return None, None


reg_exp = re.compile(r'[0-9]+')
reg_exp_url = re.compile((r'url\(\'?([A-Za-z0-9\/\.-_&;]+)\'?\)'))


def process_protocol(code, path, session, proxy, timeout=5):
    url = f'http://autocafe.co.kr/ASSO/CarCheck_Form.asp?OnCarNo={code}'''
    # url = f'http://www.autocafe.co.kr/asso/Check_Form_2020_2p.asp?Chkseq={code}'
    content, file_name = get_and_write_file(url, path,
                                            'add.html',
                                            session, proxy=proxy, timeout=timeout)
    soap = BeautifulSoup(content, 'html.parser')
    protocol_image = 1
    url_replaced = {}
    images = soap.find_all('img')
    for image in images:
        if 'src' in image.attrs:
            url_img = image.attrs['src']
            if url_img and url_img.find(';base64,') >= 0:
                continue
            if url_img and url_img.startswith('.') or url_img.startswith('/'):
                url_img = 'http://autocafe.co.kr/ASSO/' + url_img[1:]
            res, file_name = get_and_write_file_cached(url_replaced, protocol_image, url_img, path,
                                                       f'img_{protocol_image}.jpg', session, True,
                                                       'protocol',
                                                       'http://autocafe.co.kr/ASSO/', proxy=proxy, timeout=timeout)
            if res:
                image.attrs['src'] = file_name
                protocol_image += 1
    tables = soap.find_all('table', attrs={
        'title': '????????? ????????????'
    })
    if not tables:
        tables = soap.find_all('table', class_="jrPage")
    for table in tables:
        divs = table.find_all('div')
        for div in divs:
            if 'style' in div.attrs and div.attrs['style'].find('background-image:url'):
                val = reg_exp_url.findall(div.attrs['style'])
                if val:
                    url_img = val[0]

                    if url_img and url_img.find(';base64,') >= 0:
                        continue

                    if url_img and url_img.startswith('.') or url_img.startswith('/'):
                        url_img = 'http://autocafe.co.kr/ASSO/' + url_img[1:]

                    res, file_name = get_and_write_file_cached(url_replaced, protocol_image, url_img, path,
                                                               f'img_{protocol_image}.jpg', session, True,
                                                               'protocol',
                                                               'http://autocafe.co.kr/ASSO/', proxy=proxy,
                                                               timeout=timeout)
                    if res:
                        div.attrs['style'] = reg_exp_url.sub(f"url({file_name})", div.attrs['style'])
                        protocol_image += 1
    with open(f'{path}/add.html', "wb") as f_output:
        f_output.write(soap.prettify("utf-8"))


def process_additional_data(content, session, path, proxy, timeout=5):
    soap = BeautifulSoup(content, 'html.parser')
    images = soap.find_all('img')
    image_count = 1
    for image in images:
        if 'alt' not in image.attrs and (
                'onerror' in image.attrs or ('style' in image.attrs and image.attrs['style'] == 'display:none;')):
            get_and_write_file(image.attrs['src'], path, f'image_{image_count}.jpg', session, add_name_part='big',
                               timeout=timeout)
            image_count = image_count + 1
    maps = soap.find_all('map', attrs={'name': 'carPoint'})
    if maps:
        for el in maps:
            areas = el.find_all('area')
            for area in areas:
                if 'onclick' in area.attrs:
                    print(area.attrs['onclick'])
                    val = reg_exp.findall(area.attrs['onclick'])
                    if val:
                        process_protocol(val[0], path, session, proxy=proxy, timeout=timeout)
    else:
        raw_html = str(soap)
        pattern = 'http://autocafe.co.kr/ASSO/CarCheck_Form.asp?OnCarNo='
        index = raw_html.find(pattern)
        if index:
            index += len(pattern)
            car_code = []
            for i in range(20):
                if raw_html[i + index].isdigit():
                    car_code.append(raw_html[i + index])
                else:
                    break
            if car_code:
                process_protocol(''.join(car_code), path, session, proxy=proxy, timeout=timeout)


def process_car_data(object_car, path, session, proxy=None, only_detail=False, timeout=5):
    carno = object_car['CarNo']
    car_path = os.path.join(path, carno)
    if not os.path.exists(car_path):
        os.mkdir(car_path)
        file_path = os.path.join(car_path, 'car_data.json')
        with open(file_path, 'w') as file:
            file.write(json.dumps(object_car))
        image_thb = object_car['CarImageThumb']
        params = {
            'timeout': timeout
        }
        if not only_detail:
            params['proxy'] = proxy
        if image_thb:
            get_and_write_file(image_thb, car_path, f'ImageThumb.jpg', session, add_name_part='', **params)
        url = f'http://www.carmanager.co.kr/PopupFrame/CarDetail/{carno}'
        data, file_name = get_and_write_file(url, car_path, f'detail.html', session, add_name_part='', **params)
        if data:
            process_additional_data(data, session, car_path, proxy, timeout=timeout)
        for i in range(1, 6):
            key_name = f'CarMarkImageURL{i}'
            image_url = object_car[key_name]
            if image_url:
                get_and_write_file(f'http://www.carmanager.co.kr/{image_url}', car_path, f'image_{i}.gif', session,
                                   add_name_part='', timeout=timeout)


def import_car_data(login, password, db_path='DataBase', max_page=1, per_page_count=10,
                    region=103,
                    area=1035,
                    donji=94001,
                    brand=None, model=None, proxy=None, only_detail=True, timeout=5):
    if proxy and isinstance(proxy, str):
        proxy = {'http': proxy}
    sub_proxy = proxy
    if only_detail:
        proxy = None
    res, info = login2(login, password, proxy, timeout)
    if res:
        session = info
        objects = get_page_data(session, 1, per_page_count, region, area, donji, brand, model, proxy, timeout)
        if not objects:
            print('NO DATA IN RESPONSE')
            return
        total_count = objects[0]['CountTotal']
        print(f'TOTAL CARS ON SITE WITH REQUEST PARAMS {total_count}')
        for obj in objects:
            process_car_data(obj, db_path, session, proxy=sub_proxy, only_detail=only_detail)
        for i in range(2, max_page):
            objects = get_page_data(session, i, proxy=proxy, timeout=timeout)
            for obj in objects:
                for obj in objects:
                    process_car_data(obj, db_path, session, proxy=sub_proxy, only_detail=only_detail)
    else:
        print(info)


if __name__ == '__main__':
    path = os.path.join(os.path.abspath('..'), 'DataBase')
    print(path)
    import_car_data(settings.KOREA_SITE_USER, settings.KOREA_SITE_PASS, path,
                    proxy={'http': 'http://52.78.172.171:80'})
