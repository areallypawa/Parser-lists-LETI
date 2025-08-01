import requests
import json
from bs4 import BeautifulSoup as BS
from Univers import university, Ind
from CodesName import cods

def insert_data():
    """
    Выдает словарь data = { Номер ЕГПУ : [(Приоритет, [Название, Уникальный ID])]} 
    ЗАПУСКАТЬ ДЛЯ ОБНОВЛЕНИЯ ДАННЫХ ВСЕХ СПИСКОВ
    """
    data = {}
    k = 1
    for spec in cods:
        name, ids = cods[spec]
        request = requests.get(university['leti']['BASE'] + ids + '&bodyOnly=true')
        html = BS(request.content, 'html.parser')
        for el in html.select('table > tbody'):
            table = el.select('tbody > tr')
            for lines in table:
                egpu, prioritet, sogl = lines.select('tr > td')[1].get_text(), int(lines.select('tr > td')[2].get_text()), lines.select('tr > td')[13].get_text()
                if egpu in Ind:
                    # print(f'Ты тут', cods[spec], f'{egpu} твой - {myInd}',)
                    if egpu in data:
                        data[egpu] += [(prioritet, cods[spec])]
                    else:
                        data[egpu] = [(prioritet, cods[spec])]
                    break
                if str(sogl).strip() != '':
                    if egpu in data:
                        if (prioritet, cods[spec]) not in data[egpu]:
                            data[egpu] += [(prioritet, cods[spec])]
                    else:
                        data[egpu] = [(prioritet, cods[spec])]
        print(f'{name} сканирован, {k}/{len(cods)}')
        k += 1
    for el in data:
        data[el].sort()

    with open('data.json', 'w', encoding='utf-8') as f:
        print('Файл с инфой готов')
        json.dump(data, f)

data = insert_data()




