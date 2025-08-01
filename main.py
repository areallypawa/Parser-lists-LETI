import requests
import re
import json
from CodesName import cods
from test import rel
from bs4 import BeautifulSoup as BS
from log import setup_logger, logger

ans = []

# myInd = 3835101
with open('./myproject/json/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('./myproject/json/Univers.json', 'r', encoding='utf-8') as f:
    university = json.load(f)


def get_count_of_spec_mans(ind):
    """
    Выдает количество людей на специальности 
    """
    request = requests.get(university['leti']['BASE'] + ind)
    html = BS(request.content, 'html.parser')
    return int(re.search(r':\s*(\d+)', str(html.select(university['leti']['count'])[0])).group(1))


def position_in_list(ind, myInd, **kwargs):
    """
    Считает количество человек перед ТЫ кто ТОЧНО перед тобой
    """
    name = kwargs.get('name')

    setup_logger(name, myInd)

    print(f'начало работы с {name}')
    logger.info(f'начало работы с {name}')
    logger.info(' EGPU  |  НАПРАВЛЕНИЕ   |  СТАТУС  |  Счетчик')
    myPositionInList = 0
    k = 0
    request = requests.get(university['leti']['BASE'] + ind + '&bodyOnly=true')
    html = BS(request.content, 'html.parser')

    for el in html.select('table > tbody'):
        table = el.select('tbody > tr')
        for lines in table:
            if k > 130:
                return
            egpu, prioritet, sogl, = lines.select('tr > td')[1].get_text(), int(
                lines.select('tr > td')[2].get_text()), lines.select('tr > td')[13].get_text()
            if egpu == myInd:
                logger.info('ME')
                print('ME')
                ans.append(
                    (myPositionInList+1, get_count_of_spec_mans(ind), name))
                return myPositionInList + 1

            top_list_of_this_man = data.get(egpu)
            if str(sogl).strip() != '':
                if prioritet == 1 or len(top_list_of_this_man) == 1:
                    logger.info(f'{egpu} {name} СОПЕРНИК {k}')
                    k += 1
                    myPositionInList += 1
                else:
                    try:

                        if all(proverka(egpu, top_list_of_this_man[man_prioritet-1][1][1]) == 0 for man_prioritet in range(1, prioritet)):
                            logger.info(f'{egpu} {name} СОПЕРНИК {k}')
                            k += 1
                            myPositionInList += 1
                        else:

                            logger.info(f'{egpu} {name} ОТБРОС {k}')
                            for man_prioritet in range(1, prioritet):
                                try:
                                    if proverka(egpu, top_list_of_this_man[man_prioritet-1][1][1]):
                                        logger.info(
                                            f'{top_list_of_this_man[man_prioritet-1][1][0]} - он в этом списке')
                                        break
                                except:
                                    logger.error(
                                        f'{man_prioritet}, {egpu}, {top_list_of_this_man}')
                            k += 1
                    except:
                        logger.error(
                            f'ERRIR!!! {egpu}, {top_list_of_this_man}')
                        k += 1
                        myPositionInList += 1


def proverka(egpu, ind):
    request = requests.get(
        university['leti']['BASE'] + ind + '&bodyOnly=true' + '&filters%5B%5D=has_agreement')
    html = BS(request.content, 'html.parser')
    for el in html.select('table > tbody'):
        table = el.select('tbody > tr')
        for lines in table:
            num, egpu2 = int(lines.select('tr > td')[0].get_text()), lines.select(
                'tr > td')[1].get_text()
            if egpu2 == egpu:
                return num >= get_count_of_spec_mans(ind)


def solve(arr):
    Ind = university['Ind']
    Ind_Cort = university['Ind_Cort']
    for egpu in Ind:
        a = Ind_Cort[egpu]
        nums = list(map(int, a.split()))
        for el in nums:
            for i in cods:
                if arr[el] == cods[i][0]:
                    cod = cods[i][1]
                    logger.info(
                        f'{position_in_list(cod,egpu, name=cods[i][0])} / {get_count_of_spec_mans(cod)} - моя позиция в списке {cods[i][0]}')
                    # print(f'{position_in_list(cod,myInd, name=cods[i][0])} / {get_count_of_spec_mans(cod)} - моя позиция в списке',cods[i][0])

        setup_logger('', egpu, flag=1)
        for el in ans:
            logger.info(f'{el[0]} / {el[1]} {el[2]}')
            print(*el)


if __name__ == '__main__':
    print('Введи свой ЕГПУ, Нужные списки\nв файле Univers.json\nМожешь узнать код направления в файле test\n!!! работает только для сайта лэти!!!\n--Программа начала выполнение--')
    solve(rel)
