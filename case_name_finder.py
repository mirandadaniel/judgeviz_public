import mysql.connector as mysql
import pandas as pd
import os
from bs4 import BeautifulSoup 
import warnings
warnings.filterwarnings("ignore")

global successful_cases
global dictionary

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)

def strip_title(str_w_tag):
    str_wo_tag = str_w_tag.split('"')
    data = str_wo_tag[1].strip()
    data = data.replace("\'", "\'\'")
    dictionary["title"] = data
    return data

def strip_house(str_w_tag):
    str_wo_tag = str_w_tag.split('>')
    str_wo_tag = str_wo_tag[1].split('-')
    data = str_wo_tag[0].strip()
    dictionary["house"] = data
    return data

def strip_date(str_w_tag):
    str_wo_tag = str_w_tag.split('"')
    data = str_wo_tag[1].strip()
    dictionary["date"] = data
    return data

def get_metadata(case_num):
    filepath = temp_case_name
    with open(filepath) as fp:
        soup = BeautifulSoup(fp, "html.parser")
        title = soup.find("meta", attrs={'name':'Title'})
        title = str(title)
        title = strip_title(title)
        if('&amp;' in title):
            title = title.replace('&amp;', '&')
        house = soup.find("title")
        house = str(house)
        house = strip_house(house)
        date = soup.find("meta", attrs={'name':'Date'})
        date = str(date)
        date = strip_date(date)
        print(title, ' ', house, ' ', date)
        # break
        cursor = db.cursor(buffered=True)
        cursor.execute("USE graphs")
        # cursor.execute("ALTER TABLE " +  case_num + " DROP COLUMN title;")
        # cursor.execute("ALTER TABLE " +  case_num + " DROP COLUMN house;")
        # cursor.execute("ALTER TABLE " +  case_num + " DROP COLUMN date;")
        cursor.execute("ALTER TABLE " +  case_num + " ADD title varchar(1000) NOT NULL DEFAULT \'" + title + "\';")
        cursor.execute("ALTER TABLE " + case_num + " ADD house varchar(100) NOT NULL DEFAULT \'" + house + "\';")
        cursor.execute("ALTER TABLE " + case_num + " ADD date varchar(100) NOT NULL DEFAULT \'" + date + "\';")

def split_url(url):
    url = url.split('/')
    url = url[7].strip()
    url = strip_name(url)
    return url
    

def match_sql_url(f):
    # list_of_cases = ['Case 2', 'Case 6', 'Case 7', 'Case 10', 'Case 20', 'Case 25', 'Case 27', 'Case 32', 'Case 33', 'Case 35', 'Case 38', 'Case 39', 'Case 43', 'Case 47', 'Case 49', 'Case 52', 'Case 56', 'Case 66', 'Case 67', 'Case 74', 'Case 86', 'Case 87', 'Case 89', 'Case 90', 'Case 92', 'Case 100', 'Case 101', 'Case 104', 'Case 106', 'Case 107', 'Case 108', 'Case 114', 'Case 116', 'Case 121', 'Case 124', 'Case 132', 'Case 133', 'Case 134', 'Case 135', 'Case 139', 'Case 140', 'Case 145', 'Case 149', 'Case 152', 'Case 154', 'Case 157', 'Case 158', 'Case 159', 'Case 160', 'Case 162', 'Case 174', 'Case 178', 'Case 182', 'Case 190', 'Case 191', 'Case 193', 'Case 206', 'Case 207', 'Case 208', 'Case 209', 'Case 210', 'Case 211', 'Case 218', 'Case 221', 'Case 223', 'Case 225', 'Case 226', 'Case 228', 'Case 229', 'Case 232', 'Case 233', 'Case 234', 'Case 237', 'Case 240', 'Case 242', 'Case 243', 'Case 244', 'Case 246', 'Case 247', 'Case 251', 'Case 252', 'Case 253', 'Case 254', 'Case 257', 'Case 262', 'Case 267', 'Case 268', 'Case 269', 'Case 270', 'Case 271', 'Case 272', 'Case 276', 'Case 277', 'Case 284', 'Case 285', 'Case 289', 'Case 292', 'Case 296', 'Case 298'] #, 'Case 300']
    list_of_cases = ['case2', 'case3', 'case4', 'case5', 'case6', 'case7', 'case9', 'case11', 'case12', 'case13', 'case15', 'case17', 'case18', 'case19', 'case20', 'case21', 'case22', 'case23', 'case24', 'case26', 'case29', 'case31', 'case32', 'case34', 'case35', 'case36', 'case38', 'case40', 'case42', 'case43', 'case45', 'case46', 'case47', 'case49', 'case52', 'case53', 'case55', 'case56', 'case57', 'case60', 'case62', 'case63', 'case66', 'case68', 'case69']
    cursor = db.cursor(buffered=True)
    cursor.execute("USE graphs;")
    forbidden_cases = ['case14']
    # forbidden_cases = ['case154', 'case233', 'case121', 'case246', 'case67', 'case32', 'case253', 'case124', 'case32', 'case211', 'case100', 'case237', 'case134', 'case182', 'case247', 'case52', 'case178', 'case157', 'case149', 'case47', 'case225', 'case101', 'case209', 'case244', 'case139', 'case276', 'case132', 'case174', 'case207', 'case243', 'case116', 'case145', 'case162', 'case39', 'case108', 'case2', 'case133', 'case90', 'case35', 'case158', 'case232', 'case254', 'case228', 'case218', 'case49', 'case298', 'case38', 'case229', 'case66', 'case271', 'case269', 'case223', 'case152', 'case251', 'case159', 'case272', 'case262', 'case25', 'case292', 'case221', 'case240', 'case107', 'case27', 'case191', 'case252', 'case289', 'case242']
    for x in list_of_cases:
        print(x)
        # y = x.replace(' ',  '')
        # case_num = y.lower()
        if(x not in forbidden_cases):
            sql = "SELECT (body) FROM " + x + " WHERE line_col=0;"
            df = pd.read_sql(sql, con=db) 
            url = df.iloc[0, 0]
            url = split_url(url)
            if(url == f):
                successful_cases.append(x)
                print(successful_cases)
                get_metadata(x)
                # break

def strip_name(f):
    f = f.split('.htm')
    f = f[0]
    if('-' in f):
        f = f.split('-')
        f = f[0]
    if('0' in f):
        f = f.split('0')
        f = f[0]
    return f
    
global temp_case_name
dictionary = {}

directory = '/Users/mirandadaniel/Downloads/html3'
 
successful_cases = []
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    if os.path.isfile(f) and f.endswith('.htm'):
        temp_case_name = f
        f = f.split('/Users/mirandadaniel/Downloads/html3/')
        f = f[1]
        f = strip_name(f)
        match_sql_url(f) 
        # break
