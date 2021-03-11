import os

import googletrans

STANDART_DICT = {
    '하단 항목은 승용차 기준이며, 기타 자동차는 승용차에 준하여 표시': 'Приведенные ниже элементы относятся к легковому автомобилю, а другие автомобили отображаются в соответствии с автомобилем.',
    '교환·판금 등 이상 부위': 'Порченные детали, заменяемые детали и сварка',
    '자동차 기본 정보': 'Основная информация об автомобиле',
    '자동차 기본정보': 'Основная информация об автомобиле',
    '자동차 종합 상태': 'Общее состояние автомобиля',
    '자동차 종합상태': 'Общее состояние автомобиля',
    '사고·교환·수리 등 이력': 'История аварий, обменов, ремонтов и др.',
    '가격조사ㆍ산정액 및 특기사항': 'Обзор цен, сумма расчета и особые вопросы',
    '가격조사·산정액 및 특기사항': 'Обзор цен, сумма расчета и особые вопросы',
    '충전구 절연 상태': 'Состояние изоляции зарядного порта',
    '구동축전지 격리 상태': 'Состояние изоляции аккумуляторной батареи накопителя',
    '고전원전기배선 상태': 'Состояние проводки источника высокой мощности',
    '접속단자, 피복, 보호기구': 'Клемма подключения, оболочка, защитное устройство',
    '브레이크 마스터 실린더오일 누유': 'Утечка масла в главном тормозном цилиндре',
    '스티어링조인트': 'Рулевой шарнир',
    '파워고압호스': 'Шланг высокого давления силовой',
    '타이로드엔드 및 볼 조인트': 'Наконечник рулевой тяги и шаровая опора',
    '동력조향 작동 오일 누유': 'Утечка рабочего масла в гидроусилителе руля',
    '윈도우 모터': 'Стеклоподъемник',
    '실내송풍 모터': 'Электродвигатель для внутренней вентиляции',
    '와이퍼 모터 기능': 'Функция электродвигателя стеклоочистителя',
    '시동 모터': 'Стартер',
    '발전기 출력': 'Генератор',
    '스티어링 펌프': 'Насос гидроусилителя',
    '스티어링 기어': 'рулевой механизм',
    'MDPS포함': 'с MDPS',
    '라디에이터 팬 모터': 'Электродвигатель вентилятора радиатора',
    '브레이크 오일 누유': 'Утечка тормозного масла',
    '배력장치 상태': 'Износ устройства (Повышение статуса)',
    '연료누출': 'Утечка топлива',
    'LP가스포함': 'Учитывая сжиженный газ',
    '현재 주행거리': 'Текущий пробег',
    '수동변속기': 'Механическая коробка передач',
    '자동변속기': 'Автоматическая коробка передач',
    '오일유량 및 상태': 'Расход и состояние масла',
    '고전원': 'Мощьное',
    '전기장치': 'Электро оборудование',
    '자동차 세부상태': 'Подробное состояние автомобиля',
    '자동차 기타정보': 'Другая информация об автомобиле',
    '상태표시 부호': 'Обозначение состояния',
    '차대번호 표기': 'Состояние VIN кода',
    '사용이력': 'История использования',
    '배출가스': 'Выхлопной газ',
    '일산화탄소': 'монооксид углерода',
    '탄화수소': 'углеводород',
    '단순수리': 'Простой ремонт',
    '미세누유': 'Микро',
    '사용연료': 'Тип топлива',
    '자동차등록번호': 'Регистрационный номер',
    '원동기형식': 'Двигатель',
    '보증유형': 'Тип гарантии',
    '가격산정 기준가격': 'База для расчета цены',
    '최초등록일': 'Дата первоначальной регистрации',
    '무단변속기': 'Бесступенчатая трансмиссия',
    '자가보증': 'Самостоятельная гарантия',
    '보험사보증': 'Гарантия страховой компании',
    '차대번호': 'VIN код',
    '사고이력': 'История аварий',
    '유의사항 4 참조': 'См. Примечание 4',
    '유의사항 4참조': 'См. Примечание 4',
    '외판부위': 'Обшивка',
    '주요골격': 'Кузов',
    '항목': 'Предметы',
    '해당부품': 'Детали',
    '변속기': 'Трансмиссия',
    '작동상태': 'Рабочее состояние',
    '공회전': 'На холостом ходу',
    '실린더 커버': 'Крышка цилиндра',
    '로커암 커버': 'Крышка коромысла',
    '실린더 헤드': 'Головка цилиндра',
    '개스킷': 'Прокладка',
    '실린더 블록': 'Блок цилиндров',
    '오일팬': 'Маслосборник',
    '오일누유': 'Утечка масла',
    '냉각수누수': 'Утечка охлаждающей жидкости',
    '커먼레일': 'Топливная рейка (Common Rail)',
    '워터펌프': 'Помпа',
    '라디에이터서포트': 'Опора радиатора',
    '냉각수 수량': 'Количество охлаждающей жидкости',
    '미세누수': 'Микро',
    '기어변속장치': 'Переключение передач',
    '클러치 어셈블리': 'Сцепление в сборе',
    '등속조인트': 'Шарнир постоянных угловых скоростей',
    '추진축 및 베어링': 'Вал привода и подшипник',
    '디퍼렌셜 기어': 'Дифференциальная передача',
    '주행거리 및 계 기상태': 'Пробег и состояние',
    '주행거리 및 계': 'Пробег и состояние',
    '전체도색': 'Общая покраска',
    '썬루프': 'Люк на крыше',
    '네비게이션': 'навигация',
    '특별이력': 'Особая история',
    '색상변경': 'Изменение цвета',
    '수리필요': 'Нужен ремонт',
    '기본품목': 'Базовый эдемент',
    '프론트휀더': 'Переднее крыло',
    '트렁크리드': 'Крышка багажника',
    '볼트체결부품': 'Детали, крепления',
    '리어펜더': 'Заднее крыло',
    '루프패널': 'Панель крыши',
    '사이드실패널': 'Боковая панель порога',
    '쿼터패널': 'Боковины',
    '프론트패널': 'Передняя панель',
    '크로스멤버': 'Поперечина',
    '인사이드패널': 'Внутренняя панель',
    '트렁크플로어': 'Пол багажника',
    '리어패널': 'Задняя панель',
    '주요장치': 'Основное устройство',
    '자기진단': 'Самодиагностика',
    '오일 유량': 'расход масла',
    '원동기': 'Основной двигатель',
    '동력전달': 'Передача энергии',
    '사이드멤버': 'Боковой элемент',
    '휠하우스': 'Колесная арка',
    '필러패널': 'Стойка',
    '패키지트레이': 'задняя часть',
    '대쉬패널': 'приборная панель',
    '플로어패널': 'пол',
    '룸 크리닝': 'Чистка',
    '보유상태': 'в комплекте',
    '사용설명서': 'Руководство пользователя',
    '스패너': 'гаечный ключ',
    '무채색': 'Ахроматический',
    '유채색': 'Хроматический цвет',
    '조향': 'Рулевое управление',
    '연식': 'Год выпуска',
    '누수': 'Утечка',
    '제동': 'Тормоза',
    '연료': 'Топливо',
    '매연': 'дым',
    '만원': ' 10⁴₩',
    '없음': 'Нет',
    '있음': 'Да',
    '양호': 'Норм',
    '불량': 'Плохо',
    '누유': 'Утечка',
    '적정': 'Адекватно',
    '부족': 'Мало',
    '과다': 'Много',
    '차명': 'Модель',
    ' 자동\n': 'Автоматическая',
    '수동': 'Ручная',
    '세미오토': 'Полуавтоматическая',
    '기타': 'Другое',
    '가솔린': 'Бензин',
    '디젤': 'Дизель',
    'LPG': 'Газ (LPG)',
    '하이브리드': 'Гибридный',
    '수소전기': 'Водород',
    '전기': 'Электро',
    '교환': 'замена',
    '판금 또는 용접': 'листовой метал или сварка',
    '부식': 'коррозия',
    '흠집': 'царапины',
    '요철': 'вмятины',
    '손상': 'повреждение',
    ' 상태\n': 'состояние',
    '랭크': ' Классиф.',
    '후드': 'Капот',
    '도어': 'Дверь',
    '많음': 'Много',
    '보통': 'Обычно',
    '적음': 'Мало',
    '훼손': 'Поврежден',
    '상이': 'не соответсвует',
    '변조': 'Изменен',
    '변타': 'Заменен',
    '도말': 'Смазан',
    '색상': 'Цвет',
    '오손': 'Испорчен',
    '라디에이터': 'радиатор',
    '튜닝': 'модификация',
    '적법': 'законный',
    '불법': 'незаконный',
    '침수': 'утоплинник',
    '화재': 'пожар',
    '렌트': 'аренда',
    '영업용': 'Для бизнеса',
    '이행': 'выполнение',
    '미이행': 'Не выполнено',
    '외장': 'оболочке',
    '광택': 'полировке',
    '휠': 'Колесо',
    '타이어': 'шина',
    '유리': 'Стекло',
    '운전석': 'Водительское',
    '동반석': 'Посажирское',
    '잭': 'домкрат',
}


def translate_report_file(_path, _dir, translate_dict=None):
    if translate_dict is None:
        translate_dict = STANDART_DICT
    file_path = os.path.abspath(os.path.join(_path, _dir, 'add.html'))
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            with open(file_path, 'r', encoding='utf8') as file:
                content = file.read()
            if content:
                for key, val in translate_dict.items():
                    content = content.replace(key, val)
                with open(file_path, 'w', encoding='utf8') as file:
                    file.write(content)
            else:
                print(f'ERROR empty report in {_dir}')
        except Exception as e:
            print(f'ERROR in add.html dir {_dir} {e}')
    else:
        print(f'ERROR NO FILE add.html in {_dir}')


if __name__ == '__main__':
    translator = googletrans.Translator()
    print('TEST')
    path = '../DataBase/'
    test_dir = '107200888'
    translate_report_file(path, test_dir)
    translate_report_file(path, '107228417')