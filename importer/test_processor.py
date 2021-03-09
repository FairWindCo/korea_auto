import googletrans

from importer.report_processor import process_vin

if __name__ == '__main__':
    translator = googletrans.Translator()
    print('TEST')
    path ='../DataBase/'
    test_dir = '107200888'
    res = process_vin(path, test_dir, translator)
    print(res)
