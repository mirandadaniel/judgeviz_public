import csv
import mysql.connector as mysql
from mysql.connector import Error

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)
print(db)

case_numbers_list = ['case3', 'case5', 'case11', 'case22', 'case24', 'case29', 'case31', 'case34', 'case36', 'case40', 'case46', 'case55', 'case62', 'case68']
allowed_cases = ['case14']
cursor = db.cursor(buffered=True)
cursor.execute("USE graphs")
file_path = '/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz5/graph_files/ai_files/'
for x in case_numbers_list:
    if x in allowed_cases:
       
        complete_filename = file_path + x + '.tsv'
        sql1 = "CREATE TABLE " + x + " (case_num VARCHAR(50), line_col VARCHAR(50), body varchar(5000), from_col VARCHAR(50), to_col VARCHAR(50), relation_col VARCHAR(50), pos_col VARCHAR(50), mj_col VARCHAR(50));"
        cursor.execute(sql1)
        with open(complete_filename) as file:
            case_file = csv.reader(file, delimiter="\t")
            for line in case_file:
                sql = "INSERT INTO " + x + " (case_num, line_col, body, from_col, to_col, relation_col, pos_col, mj_col) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7]) 
                cursor.execute(sql, val)

db.commit()