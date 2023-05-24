import requests
import mysql.connector as mysql
import pandas as pd
import os
import warnings
import re
import shutil
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")

global line_arr
line_arr = []

global disa_line_cols
disa_line_cols = []

def highlight_all_rels(row):
    value = row.loc['relation_col']
    color = ''
    return ['background-color: {}'.format(color) for r in row]

def make_full_disa(from_j, to_j, line_col):
    from_j = from_j.upper()
    if('all' not in to_j):
        to_j = to_j.upper()
    line = '<br/> <br/>' + from_j + ' fully disagreed with ' + to_j + '\n\n\n\n'
    disa_line_cols.append(line_col)
    return line

def make_part_disa(from_j, to_j, line_col):
    from_j = from_j.upper()
    if('all' not in to_j):
        to_j = to_j.upper()
    line = '<br/> <br/>' + from_j + ' partially disagreed with ' + to_j + '\n\n\n\n'
    disa_line_cols.append(line_col)
    return line

def make_disa(relation, from_j, to_j, line_col):
    if('fulldisa' in relation):
        line = make_full_disa(from_j, to_j, line_col)
        return line
    if('partdisa' in relation):
        line = make_part_disa(from_j, to_j, line_col)
        return line

def add_disagrements(content, df):
    total = len(content)
    for index, row in df.iterrows():
        relation = row.loc['relation_col']
        from_j = row.loc['from_col']
        to_j = row.loc['to_col']
        line_col = row.loc['line_col']
        if('fulldisa' in relation or 'partdisa' in relation):
            line = make_disa(relation, from_j, to_j, line_col)
            if(content[total-1] != line):
                content.insert(total-1, line) 
            if('}' in content[total]):
                content[total] = content[total].replace('}', '')
    return content

def match_align_to_sentence(content, df_new):
    total = len(content)
    for index, row in df_new.iterrows():
        align_num = row['align']
        sentence_num = row['asmo_sent_id']
        body = row['case_text']
        if('NONE' not in align_num):
            align_num = int(align_num)
            old_line = content[align_num-1]
            new_line = "<a id=\"bbb{}\">".format(sentence_num) + old_line + "</a>"
            content[align_num-1] = new_line
            line_arr.append(sentence_num)
    return content

def add_hrefs_to_content(content, df, case_num, dbConnection):
    content = content.split('.')
    count = 1
    table_name = 'text_' + case_num
    df_new = pd.read_sql('SELECT * FROM all_data.{}'.format(table_name), dbConnection)
    content = match_align_to_sentence(content, df_new)
    content = add_disagrements(content, df)
    return content

def get_content():
    file = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/static/graph_summary.html"
    txt_file = open(file, "r")
    file_content = txt_file.read()
    content_list = file_content.split("<hr/>")
    txt_file.close()
    content_list = content_list[1].replace('<p>', '')
    content_list = content_list.replace('</p>', '')
    content_list = content_list.replace('</td>', '')
    content_list = content_list.replace('</tr>', '')
    content_list = content_list.replace('<tr>', '')
    content_list = content_list.replace('<td>', '')
    return content_list

def write_to_file2(text):
    directory = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/static/"
    full_file = directory + 'graph_summary.html'
    text = '.'.join(text)
    fp= open(full_file, 'w')
    fp.write(text)
    fp.write('<br/> <br/> <br/>')
    fp.close()

def write_to_file(text):
    directory = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/static/"
    full_file = directory + 'graph_summary.html'
    fp= open(full_file, 'w')
    for line in text:
        if('img' not in line):
            if('http://www' not in line):
                if("font color=\"lime\"" in line):
                    line = line.replace("lime", "black")
                if("font color=\"#33FF33\"" in line):
                    line = line.replace("#33FF33", "black")
                fp.write(line)
    fp.close()


def extract_summary(filename):
    directory = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/metadata/"
    full_file = directory + filename
    with open(full_file, "r", encoding='unicode_escape') as fp:
        soup = BeautifulSoup(fp, 'html.parser', from_encoding='unicode_escape')
        body = soup.findAll('body')
        table = soup.find('table')
        rows = table.findAll(lambda tag: tag.name=='tr')
        table_arr = []
        for r in rows:
            r = str(r)
            table_arr.append(r)
    return table_arr

def find_file_match(date_match, name_check):
    name_check = name_check.lower() 
    name_check = name_check.split()
    date_match = '_'.join(date_match)
    directory = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/metadata/"
    for filename in os.listdir(directory):
        if filename.endswith(".htm"):
            if date_match in filename:
                new_filename = filename.split('.htm')
                new_filename = new_filename[0].split('_')
                new_filename = new_filename[3]
                for name in name_check:
                    if new_filename in name:
                        return filename 
    

def find_date_match(date_check):
    date_check = date_check.lower()
    date_check = date_check.split()
    if(date_check[0].startswith('0')):
        date_check[0] = date_check[0].lstrip("0")
    directory = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/metadata/"
    best_match = ' '
    highest_count = 0
    for filename in os.listdir(directory):
        if filename.endswith(".htm"):
            count = 0
            filename = filename.split('.')
            filename = filename[0].split('_')
            date = []
            date.append(filename[0])
            date.append(filename[1])
            date.append(filename[2]) 
            for d in date:
                for c in date_check:
                    if(c == d):
                        count+=1
                        if(count == 3):
                            return date

                       
def make_summary(date, name, case_num, df, dbConnection):                    
    date_match = find_date_match(date)
    filename = find_file_match(date_match, name)  
    text = extract_summary(filename) 
    write_to_file(text)
    content = get_content()
    content = add_hrefs_to_content(content, df, case_num, dbConnection)
    write_to_file2(content)

def make_summary_graph(df, case_name):
    global all_flag
    global pass_judge_dict
    all_flag = False
    judge_dict = parse_file(df)
    pass_judge_dict = judge_dict
    create_dot_file(judge_dict, case_num)

def edit_map_file_numbers(map_file):
    new_map_file = ''
    map_file = map_file.split('\n')
    for line in map_file:
        if('href="' in line and "alt=\"\"" in line): 
            line = line.replace('href=\"#', 'href=\"#bbb')
            new_map_file =  new_map_file + line + '\n'
        else:
            line = line.replace('alt=\"', 'alt=\"bbb')
            new_map_file =  new_map_file + line + '\n'
    return new_map_file

def edit_map_file(map_file):
    new_map_file = ''
    map_file = map_file.split('\n')
    for line in map_file:
        if('href="fullagr' in line or 'href="partagr' in line or 'href="fulldisa' in line or 'href="partdisa' in line or 'href="outcome' in line):
            line = line.replace('href', 'alt')
            line = line.replace('alt=\"\"', '')
            line_temp = line.split('/>')
            line = line_temp[0] + ' onclick="myFunction(this.alt)"/>'
            new_map_file =  new_map_file + line + '\n'
        new_map_file =  new_map_file + line + '\n'
    return new_map_file


def make_map(case_num, map_file):
    map_file = edit_map_file(map_file)
    map_file = edit_map_file_numbers(map_file)
    return map_file
