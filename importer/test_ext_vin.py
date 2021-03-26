import os

from importer.report_processor import extract_vin, extract_year, extract_driven

if __name__ == "__main__":
    dirs = [f for f in os.listdir('../DataBase') if os.path.isdir(os.path.join('../DataBase', f))]
    for dir in dirs:
        with open(os.path.join('../DataBase', dir, 'add.html'), encoding='utf8') as file:
            content = file.read()
            print(dir, extract_vin(content), extract_driven(content), extract_year(content))