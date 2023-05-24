import csv
import mysql.connector as mysql
from mysql.connector import Error

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)
print(db)


case_numbers_list = ['11', '9', '12', '13', '5', '20', '3', '2', '21', '7', '4', '15', '18', '19', '17', '42', '38', '26', '45', '43', '31', '35', '36', '32', '40', '29', '24', '34', '47', '69', '55', '63', '57', '62', '46', '60', '49', '56', '66', '68', '52', '53']
cursor = db.cursor(buffered=True)
cursor.execute("USE all_data")
with open('case63.tsv') as file:
    case_file = csv.reader(file, delimiter="\t")
    for line in case_file:
        sql = "INSERT INTO text_case63 (case_id, asmo, asmo_sent_id, sentence_id, para_id, judge, case_text, role, align, agree, outcome, ackn, provision_ent, instrument_ent, court_ent, case_name_ent, citation_bl_ent, judge_ent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10], line[11], line[12], line[13], line[14], line[15], line[16], line[17])
        cursor.execute(sql, val)

db.commit()