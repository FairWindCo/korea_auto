import requests

if __name__ == '__main__':
    print('start')
#                      'http://autocafe.co.kr/ASSO/CarCheck_Form.asp?OnCarNo='
    res= requests.get('http://autocafe.co.kr/ASSO/CarCheck_Form.asp?OnCarNo=202140024564', proxies={
        'http':'http://52.78.172.171:80'
    })
    if res and res.status_code==200:
        print(res.text)
    else:
        print(res)
    res = requests.get('http://www.autocafe.co.kr/asso/Check_Form_2020_2p.asp?Chkseq=202140024564', proxies={
        'http': 'http://52.78.172.171:80'
    })
    if res and res.status_code==200:
        print(res.text)
    print('finish')
