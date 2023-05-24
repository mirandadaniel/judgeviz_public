import mysql.connector as mysql
import pandas as pd
from bs4 import BeautifulSoup

import webbrowser


# webbrowser.open('http://net-informations.com', new=2)

# global dictionary #= {}

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)

cursor = db.cursor(buffered=True)
cursor.execute("USE graphs;")
case_names = ['case2', 'case3', 'case4', 'case5', 'case6', 'case7', 'case9', 'case11', 'case12', 'case13', 'case14', 'case15', 'case17', 'case18', 'case19', 'case20', 'case21', 'case22', 'case23', 'case24', 'case26', 'case29', 'case31', 'case32', 'case34', 'case35', 'case36', 'case38', 'case40', 'case42', 'case43', 'case45', 'case46', 'case47', 'case49', 'case52', 'case53', 'case55', 'case56', 'case57', 'case60', 'case62', 'case63', 'case66', 'case68', 'case69']

urls_list = []
for x in case_names: 
    x = x.replace(' ',  '')
    x = x.lower()
    sql = "SELECT (body) FROM " + x + " WHERE line_col=0;"
    df_2 = pd.read_sql(sql, con=db) 
    url = df_2.iloc[0, 0]
    urls_list.append(url)

urls_list = '\n'.join(urls_list)
with open('urls2.txt', 'w') as f:
    f.write(urls_list)