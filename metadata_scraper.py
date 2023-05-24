import requests
import mysql.connector as mysql
import pandas as pd
import os
from bs4 import BeautifulSoup 
import warnings
import re
import format_dataframe as fd
import fileinput
import nltk.data


global line_arr
line_arr = []

global disa_line_cols
disa_line_cols = []


def highlight_all_rels(row):
    color = ''
    return ['background-color: {}'.format(color) for r in row]

def format_case_text(df):
    for index, row in df.iterrows(): 
        body = row.loc['body']
        line_col = row.loc['line_col']
        for number in line_arr:
            if number == line_col or line_col in disa_line_cols:
                if("<p" in body):
                    body = body.replace("<p", "<a")
                    body = body.replace("</p>", "</a>")
                    body = body.replace("id=\"", "id=\"aaa")
                    df.at[index, 'body']=body
                else:
                    value = "<a id=\"aaa{}\">".format(line_col) + body + "</a>"
                    df.at[index, 'body']=value
    return df

def make_full_disa(from_j, to_j, line_col):
    from_j = from_j.upper()
    if('all' not in to_j):
        to_j = to_j.upper()
    line = '<br/> <br/>' + from_j + ' fully disagreed with ' + to_j
    line = line + "<a href=\"#aaa{}\"  onclick=\"highlightLinks(href);\">".format(line_col) + " [" + line_col + "] " + "</a>" + "\n\n\n\n"
    disa_line_cols.append(line_col)
    return line

def make_part_disa(from_j, to_j, line_col):
    from_j = from_j.upper()
    if('all' not in to_j):
        to_j = to_j.upper()
    line = '<br/> <br/>' + from_j + ' partially disagreed with ' + to_j 
    line = line + "<a href=\"#aaa{}\"  onclick=\"highlightLinks(href);\">".format(line_col) + " [" + line_col + "] " + "</a>" + '\n\n\n\n'
    disa_line_cols.append(line_col)
    return line

def make_disa(relation, from_j, to_j, line_col):
    if('fulldisa' in relation):
        line = make_full_disa(from_j, to_j, line_col)
        return line
    if('partdisa' in relation):
        line = make_part_disa(from_j, to_j, line_col)
        return line

def remove_duplicate_disagreements(disagreements):
    prev_d = ['', '', '', '']
    line = ''
    prev_line = ''
    for d in disagreements:
        if(d[0] == prev_d[0] and d[1] == prev_d[1] and d[2]==prev_d[2]):
            line = prev_line + "<a href=\"#aaa{}\" onclick=\"highlightLinks(href);\">".format(d[3]) + " [" + d[3] + "] " + "</a>"
            prev_line = line
            prev_d = d
        else:
            line = make_disa(d[0], d[1], d[2], d[3])
            prev_d = d
            prev_line = line
    return line
    
def add_disagrements(content, df):
    total = len(content)
    disagreements = []
    for index, row in df.iterrows():
        relation = row.loc['relation_col']
        from_j = row.loc['from_col']
        to_j = row.loc['to_col']
        line_col = row.loc['line_col']
        if('fulldisa' in relation or 'partdisa' in relation):
            data = [relation, from_j, to_j, line_col]
            disagreements.append(data)
    line = remove_duplicate_disagreements(disagreements)
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
        if('NONE' not in align_num and 'no match' not in sentence_num):
            align_num = int(align_num)
            old_line = content[align_num-1]
            if("href=\"#aaa{}\"".format(sentence_num) not in old_line):
                new_line = old_line + "<a href=\"#aaa{}\" onclick=\"highlightLinks(href);\">".format(sentence_num) + " [" + sentence_num + "] " + "</a>"
                content[align_num-1] = new_line
                line_arr.append(sentence_num)
    return content

def add_hrefs_to_content(content, df, case_num, dbConnection):
    count = 1
    for line in content:
        count+=1
    table_name = 'text_' + case_num
    df_new = pd.read_sql('SELECT * FROM all_data.{}'.format(table_name), dbConnection)
    content = match_align_to_sentence(content, df_new)
    content = add_disagrements(content, df)
    return content

def get_content(case_num):
    file = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/static/summary.html"
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
    content_list = content_list.replace('.<br>', '. <br>')
    content_list = content_list.replace('.<', '. <')
    return content_list

def remove_double_stop(text):
    if(".." in text):
        text = text.replace("..", ".")
    if("</a>.<a" in text):
        text = text.replace("</a>.<a", "</a><a")
    if('and!'in text):
        text = text.replace('and!', 'and ')
    text = text + '<br/> <br/> <br/>'
    return text

def write_to_file2(text):
    directory = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/static/"
    full_file = directory + 'summary.html'
    text = ' '.join(text)
    text = remove_double_stop(text)
    fp= open(full_file, 'w')
    fp.write(text)
    fp.close()
    
def write_to_file(text):
    directory = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/static/"
    full_file = directory + 'summary.html'
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
                d = d.strip()
                for c in date_check:
                    c = c.strip()
                    if(c == d):
                        count+=1
                        if(count == 3):
                            return date

def split_into_sentences(content):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    data = content
    content = '--------'.join(tokenizer.tokenize(data))
    content_arr = content.split('--------')
    return content_arr


def main(date, name, case_num, df, dbConnection):                
    date_match = find_date_match(date)
    filename = find_file_match(date_match, name)  
    text = extract_summary(filename) 
    write_to_file(text)
    content = get_content(case_num)
    content = split_into_sentences(content)
    content = add_hrefs_to_content(content, df, case_num, dbConnection)
    write_to_file2(content)
    df = fd.format_dataframe_summary_text(df)
    df = format_case_text(df)
    summary_styled_table = df.style.apply(highlight_all_rels, axis=1).hide([('case_num'), ('from_col'), ('to_col'), ('pos_col'), ('mj_col'), ('title'), ('house'), ('date')], axis="columns").hide_columns().hide_index()
    summary_styled_table.to_html('static/summary_links.html')
    fp= open('static/summary_links.html', 'a')
    fp.write('<br><br><br>')
    fp.close()