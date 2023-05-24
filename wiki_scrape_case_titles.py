import requests
import mysql.connector as mysql
import pandas as pd
import os
from bs4 import BeautifulSoup 
import warnings
import re
warnings.filterwarnings("ignore")

global swag_count
global successful_cases
successful_cases = []

def get_title(x):
    if('href' not in x):
        title = x.split('<li><i>')
        title = title[1].split('</i>')
        title = title[0].replace('&amp;', '&')
        title = title.replace('\'', '\'\'')
        return title
    else:
        title = x.split('">')
        title = title[1].split('</i>')
        title = title[0].replace('&amp;', '&')
        title = title.replace('</a>', '')
        title = title.replace('\'', '\'\'')
        return title

def get_year(data):
    data = data.split('[')
    date = data[1].split(']')
    date = date[0]
    return date

def get_house(data):
    data = data.split(' ')
    house = data[1]
    return house

def add_to_sql(data, x, case_num):
    title = get_title(x)
    year = get_year(data)
    house = get_house(data)
    cursor = db.cursor(buffered=True)
    cursor.execute("USE case_text")
    # # cursor.execute("ALTER TABLE " +  case_num + " DROP COLUMN title;")
    # # cursor.execute("ALTER TABLE " +  case_num + " DROP COLUMN house;")
    # # cursor.execute("ALTER TABLE " +  case_num + " DROP COLUMN date;")
    cursor.execute("ALTER TABLE " +  case_num + " ADD title varchar(1000) NOT NULL DEFAULT \'" + title + "\';")
    cursor.execute("ALTER TABLE " + case_num + " ADD house varchar(100) NOT NULL DEFAULT \'" + house + "\';")
    cursor.execute("ALTER TABLE " + case_num + " ADD date varchar(100) NOT NULL DEFAULT \'" + year + "\';")
    successful_cases.append(case_num)

def match_data_to_wiki(data, case_num):
    swag_count = 0
    URL = "https://en.wikipedia.org/wiki/List_of_House_of_Lords_cases#2001"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    all_list_items = soup.find(id="bodyContent").find_all("li")
    for x in all_list_items:
        x = str(x)
        if data in x:
            swag_count+=1
            return x

def get_case_data(): 
    cursor = db.cursor(buffered=True)
    cursor.execute("USE case_text;")
    list_of_cases = ['Case 22', 'Case 23', 'Case 11', 'Case 12', 'Case 14', 'Case 13', 'Case 5', 'Case 20', 'Case 3', 'Case 2', 'Case 21', 'Case 7', 'Case 4', 'Case 15', 'Case 18', 'Case 19', 'Case 6', 'Case 17', 'Case 42', 'Case 38', 'Case 26', 'Case 45', 'Case 43', 'Case 31', 'Case 35', 'Case 36', 'Case 32', 'Case 40', 'Case 29', 'Case 24', 'Case 34', 'Case 47', 'Case 69', 'Case 55', 'Case 57', 'Case 62', 'Case 46', 'Case 60', 'Case 49', 'Case 56', 'Case 66', 'Case 68', 'Case 52']
    forbidden_cases = ['case22', 'case23', 'case11', 'case12', 'case14', 'case13', 'case5', 'case20', 'case3', 'case2', 'case21', 'case7', 'case4', 'case15', 'case18', 'case19', 'case6', 'case17', 'case42', 'case38', 'case26', 'case45', 'case43', 'case31', 'case35', 'case36', 'case32', 'case40', 'case29', 'case24', 'case34', 'case47', 'case69', 'case55', 'case57', 'case62', 'case46', 'case60', 'case49', 'case56', 'case66', 'case68', 'case52']
    for x in list_of_cases:
        y = x.replace(' ',  '')
        case_num = y.lower()
        if(case_num not in forbidden_cases):
            sql = "SELECT (case_text) FROM " + y + " WHERE sentence_id=0;"
            df = pd.read_sql(sql, con=db) 
            data = df.iloc[0, 0]
            tag = match_data_to_wiki(data, case_num)
            add_to_sql(data, tag, case_num)

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)

get_case_data()
