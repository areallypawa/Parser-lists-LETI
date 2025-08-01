import requests
from bs4 import BeautifulSoup as BS
from Univers import university


def get_code_name():
    """
    Выдает словарь cods = { Номер направления : Уникальный id к ссылке }
    """
    cods = {}
    request = requests.get(university['leti']['root'])
    html = BS(request.content, 'html.parser')
    for el in html.select(f"{university['leti']['h1']} > {university['leti']['h2']}"):
        table = el.select(f"{university['leti']['h3']} > {university['leti']['h4']} > tr")
        for lines in table[2:]:
            code, name, g = [i for i in lines.select('tr > td')]
            code, name = code.get_text(), name.get_text()
            ids = g.find('a')['href'][57:]
            if code in cods:
                cods[code + ' '] = [name, ids]
            else:
                cods[code] = [name, ids]

    return cods
cods = get_code_name()
