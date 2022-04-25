import pymysql as pymysql
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

'''модуль считывания названий групп VK и сохранение их в БД  MySQL локально на ПК)'''

# ----- стартовый URL на VK
url = 'https://vk.com/groups/recommendations'

# ---- подключаем Селениум (драйвер chromedriver.exe в корне С:\)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
s = Service('C:/chromedriver.exe')
driver = webdriver.Chrome(service=s, options=options)


#------ создам БД vk_base-----------------

# ----- подключаемся к локальной БД ----
login = 'root'
user_password = 'Tino4ka'
dbase = 'vk_base'

my_db = pymysql.connect(
    host='localhost',
    user=login,
    passwd=user_password,
    database=dbase,
    cursorclass=pymysql.cursors.DictCursor
    )
mycursor = my_db.cursor()

# ----  запрос на создание таблицы -----
sql_new_table = "CREATE TABLE IF NOT EXISTS vk_group (" \
                "id INT,  " \
                "type text,  " \
                "name_group text,  " \
                "avatar_group text, " \
                "quantity_group INT)"

# ----- запрос на добавление в БД -------------
sql_insert_data = f"INSERT INTO vk_group (id, type, name_group, avatar_group, quantity_group) VALUES (%s, %s, %s, %s, %s)"

mycursor.execute(sql_new_table)
my_db.commit()

driver.get(url)


groups = driver.find_elements(By.XPATH, '//div[@class="groups_row search_row clear_fix"]')

group_dict = []
for i in groups:
    data_group = {}
    # ---- получение id-группы --------
    try:
        id = i.get_attribute('data-id')
    except:
        id = ''
    # ---- получение URL avatar-группы --------
    try:
        avatar = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
    except:
        avatar = ''
    # ---- получение названия-группы --------
    try:
        name = i.text.split('\n')[1]
    except:
        name = ''
    # ---- получение типа-группы --------
    try:
        type_group = i.text.split('\n')[2]
    except:
        type_group = ''
    # ---- получение кол-ва подписчиков-группы --------
    try:
        quantity = i.text.split('\n')[3]
        quantity = int(' '.join(quantity.split(' ')[:-1]).replace(' ', ''))
    except: quantity = ''

    # ----- сохраним в словарь группы------
    data_group['id'] = id
    data_group['type'] = type_group
    data_group['avatar'] = avatar
    data_group['name'] = name
    data_group['quantity'] = quantity

    # ----- внесем данные в БД-----
    # mycursor.execute(sql_insert_data, list(i.values()))
    mycursor.execute(sql_insert_data, list(list(data_group.values())))
    my_db.commit()
    # ----- сохраним словарь в список ГРУПП-----
    group_dict.append(data_group)

driver.close()
pprint(group_dict)





