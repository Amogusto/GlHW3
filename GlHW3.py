import pymongo
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError
import requests
from bs4 import BeautifulSoup
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['vc']
# #1
vcncy = db.vcncy
#vcncy.delete_many({})

def update(vacancy_info):
    db.vcncy.update_one(
        {'name': vacancy_info['name'], 'link': vacancy_info['link'], },
        {'$set': {'name': vacancy_info['name'], 'max_salary': vacancy_info['max_salary'],
         'min_salary': vacancy_info['min_salary']}}, upsert=True)

url = 'https://kazan.hh.ru/search/vacancy?text=&area=88'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.4.837 Yowser/2.5 Safari/537.36'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

vacancys = soup.find_all('div', {'class': 'vacancy-serp-item__layout'})
#vcncy.delete_many({})
vacancys_list = []
for vacancy in vacancys:
    vacancy_info = {}
    print()
    info = vacancy.find('a', {'class': 'serp-item__title'})
    name = info.text
    link = info.get('href')
    salary = vacancy.find('span', {'class': 'bloko-header-section-2'})
    try:
        salary = salary.text.split()


        if salary[0] == 'до':
            s_min = None
            s_max = int(salary[1] + salary[2])
            currency = salary[3]
        elif salary[0] == 'от':
            s_min = int(salary[1] + salary[2])
            s_max = None
            currency = salary[3]
        else:
            s_min = int(salary[0] + salary[1])
            s_max = int(salary[3] + salary[4])
            currency = salary[5]
    except:
        vacancy_info['name'] = name
        vacancy_info['link'] = link
        vacancy_info['source'] = 'hh.ru'
        vacancy_info['max_salary'] = None
        vacancy_info['min_salary'] = None
        vacancy_info['currency'] = None

    vacancy_info['name'] = name
    vacancy_info['link'] = link
    vacancy_info['source'] = 'hh.ru'
    vacancy_info['max_salary'] = s_max
    vacancy_info['min_salary'] = s_min
    vacancy_info['currency'] = currency
    vacancys_list.append(vacancy_info)
#    db.vcncy.insert_one(vacancy_info)
    #update(vacancy_info)
#    db.vcncy.update_one({'name': vacancy_info['name'], 'link': vacancy_info['link'], 'max_salary': vacancy_info['max_salary'], 'min_salary': vacancy_info['min_salary']},
#                        {'$set': {'name': vacancy_info['name']}}, upsert=True)
#        pprint(db.vcncy.find({name:vacancy_info['name']}, {link:vacancy_info['link']}))

bom = {'name': 'Менеджер по продажкам',
  'link': 'https://adsrv.hh.ru/click?b=558372&c=30&place=35&meta=ok2Kwlx1enxyapo3nsplHRdf2mQdjKBF_YnsbmB6Ag5v7pphzGXjs5vsAPKlLfcPCnoHVtvj9g63qJOxBEWJ6UIWA7pOaiogc6GuQ7f2kWcvvnVAyEPZ3wHEdrbL7IIkjD98a7ntfHwAx7lrzrK3GTAlL_ZqbUoXJSs4A0XIm6pYQQJ-UiJ7xlOqtxReV5ko_aE5McthKvLZmbKBYAYSarZ8fQFKiCw6SuW5PhKNLLOD68rsUJ0-Sz0E3xTG3guQgdfP3BhU4gOz-RjCRoky2arUQEahUtLFhLgNUMyOiDNcbh6xlSfssTTYzVJfF5y8TMO5fGqJ5Pb46I4Zg1A2s5K3nruARDFvFUa6fUPgq8bWR484jWopOj8zQVwDLFDmRVVjYIixvqtmU6M7NOnmYOF1gi4ei-P_uCRSM3kS9nQImK8JobXJ8giMdhM4QBJx2HExE5dLRKgk5YYimPsVhfu8k7TaomT5tdakaWTN6xTipZIhor_5CnWk0MHbkor7ceDRj1R4OWSCG486a78T4Q%3D%3D&clickType=link_to_vacancy',
  'source': 'hh.ru',
  'max_salary': 111111111,
  'min_salary': 0,
  'currency': '₽'}

update(bom)

#for vacancy_info in vcncy.find({}):
 #   pprint(vacancy_info)



# #2

for vacancy_info in vcncy.find(
        {'$or': [{'max_salary': {'$gte': 100000}}, {'min_salary': {'$gte': 100000}}]}):

    pprint(vacancy_info)
