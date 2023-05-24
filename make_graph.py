from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import mysql.connector as mysql
from flask_cors import CORS
import numpy as np
import pandas as pd
import pydot
import os
import cv2
from mysql.connector import Error
from string import ascii_lowercase
import re
import warnings
import codecs
import pydot
from IPython.display import display
import config as c
warnings.filterwarnings("ignore")

def strip_title(judge):
    if(' ' in judge):
        judge = judge.split(' ')
        judge = '\"' + judge[1] + '\"'
        return judge
    else:
        judge = judge
        return judge

def make_fullagr_edge(judge, count):
    if(judge['to'] == 'all'):
        all_flag == True
    judge_from = strip_title(judge['from'])
    judge_to = strip_title(judge['to'])
    name = 'fullagr_' + judge_from.strip('\"') + '_' + judge_to.strip('\"') + '_' + judge['line_number']
    if(judge['to'] == 'self'):
        line = judge_from, '->', '{', judge_from, '}', '[color="darkgreen", arrowhead="normal", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
    else:
        line = judge_from, '->', '{', judge_to, '}', '[color="darkgreen", arrowhead="normal", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
    return line

def make_partagr_edge(judge):
    if(judge['to'] == 'all'):
        all_flag == True
    judge_from = strip_title(judge['from'])
    judge_to = strip_title(judge['to'])
    name = 'partagr_' + judge_from.strip('\"') + '_' + judge_to.strip('\"') + '_' + judge['line_number']
    line = strip_title(judge['from']), '->', '{', strip_title(judge['to']), '}', '[color="darkgreen", arrowhead="onormal", penwidth=1, href=\"{}\"];'.format(name), '\n'
    line = ' '.join(line)
    line = ' ' + line
    return line

def make_fulldis_edge(judge):
    if(judge['to'] == 'all'):
        all_flag == True
    judge_from = strip_title(judge['from'])
    judge_to = strip_title(judge['to'])
    name = 'fulldisa_' + judge_from.strip('\"') + '_' + judge_to.strip('\"') + '_' + judge['line_number']
    line = strip_title(judge['from']), '->', '{', strip_title(judge['to']), '}', '[color="red", arrowhead="dot", penwidth=1, href=\"{}\"];'.format(name), '\n'
    line = ' '.join(line)
    line = ' ' + line
    return line

def make_partdis_edge(judge):
    if(judge['to'] == 'all'):
        all_flag == True
    judge_from = strip_title(judge['from'])
    judge_to = strip_title(judge['to'])
    name = 'partdisa_' + judge_from.strip('\"') + '_' + judge_to.strip('\"') + '_' + judge['line_number']
    line = strip_title(judge['from']), '->', '{', strip_title(judge['to']), '}', '[color="red", arrowhead="odot", penwidth=1, href=\"{}\"];'.format(name), '\n'
    line = ' '.join(line)
    line = ' ' + line
    return line

def make_outcome_edge(judge):
    if(judge['to'] == 'all'):
            all_flag == True
    judge_from = strip_title(judge['from'])
    judge_to = strip_title(judge['to'])
    name = 'outcome_' + judge_from.strip('\"') + '_' + judge_to.strip('\"') + '_' + judge['line_number']
    if(judge['to'] == 'self'):
        line = strip_title(judge['from']), '->', '{', strip_title(judge['from']), '}', '[color="blue", arrowhead="vee", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line
    else:
        line = strip_title(judge['from']), '->', '{', strip_title(judge['to']), '}', '[color="blue", arrowhead="vee", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line

def make_factagr_edge(judge):
    judge_from = strip_title(judge['from'])
    judge_to = strip_title(judge['to'])
    name = 'factagr_' + judge_from.strip('\"') + '_' + judge_to.strip('\"') + '_' + judge['line_number']
    if(judge['to'] == 'all'):
            all_flag == True
    if(judge['to'] == 'self'):
        line = strip_title(judge['from']), '->', '{', strip_title(judge['from']), '}', '[color="grey", arrowhead="normal", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line
    else:
        line = strip_title(judge['from']), '->', '{', strip_title(judge['to']), '}', '[color="grey", arrowhead="normal", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line

def make_ackn_edge(judge):
    judge_from = strip_title(judge['from'])
    judge_to = strip_title(judge['to'])
    name = 'ackn_' + judge_from.strip('\"') + '_' + judge_to.strip('\"') + '_' + judge['line_number']
    if(judge['to'] == 'all'):
            all_flag == True
    if(judge['to'] == 'self'):
        line = strip_title(judge['from']), '->', '{', strip_title(judge['from']), '}', '[color="yellow", arrowhead="normal", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line
    else:
        line = strip_title(judge['from']), '->', '{', strip_title(judge['to']), '}', '[color="yellow", arrowhead="normal", penwidth=1, href=\"{}\"];'.format(name), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line

def add_edge(judge, count):
    if(judge['relation'] == 'fullagr'):
        edge = make_fullagr_edge(judge, count)
        return edge
    if(judge['relation'] == 'partagr'):
        edge = make_partagr_edge(judge)
        return edge
    if(judge['relation'] == 'fulldisa'):
        edge = make_fulldis_edge(judge)
        return edge
    if(judge['relation'] == 'partdisa'):
        edge = make_partdis_edge(judge)
        return edge
    if(judge['relation'] == 'outcome'):
        edge = make_outcome_edge(judge)
        return edge

def make_edges(dot_file):
    count = 1
    global count_arr
    count_arr = []
    checker = []
    for judge in c.judge_dict:
        edge = add_edge(judge, count)
        edge_check = edge.split('href=')
        if edge_check[0] not in dot_file:
            num = edge_check[1].split('_')
            num = '\"#' + num[3] #+ '"]; \n'
            edge = edge.replace(edge_check[1], num)
            dot_file = dot_file + edge
            prev_edge = edge_check[0]
            count_arr.append(count)
            count+=1
        elif edge_check[0] in dot_file:
                name = edge_check[1].split('_')
                name = name[0] + '_' + name[1] + '_' + name[2] 
                if('-' in name):
                    name = name.replace('-', '')
                c.all_mini_files.append(name.strip('\"'))
                name = name + '"];'
                num = name[3]
                dot_file = dot_file.split('\n')
                length = len(dot_file)
                index = length-1
                replacement_edge = edge_check[0] + 'href=' + name
                check = ''
                for line in dot_file:
                    if edge_check[0] in line:
                        check = line
                dot_file = ('\n').join(dot_file)
                dot_file = dot_file.replace(check, replacement_edge)
    return dot_file

# check meeeee! 
def make_line_mo(judge):
    temp_mo = c.mo_judges
    temp_mo2 = []
    for mo in temp_mo:
        mo = trim_judge(mo)
        temp_mo2.append(mo)
    if (judge in temp_mo2):
        judge = judge.replace('lord', '')
        judge = judge.strip('\"')
        line = ' \"' + judge + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="yellow", href=\"#{}\"]; \n'.format(judge.strip('\"'))
        return line
    else:
        judge = judge.replace('lord', '')
        judge = judge.strip('\"')
        line = ' \"' + judge + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href=\"#{}\"]; \n'.format(judge.strip('\"'))
        return line

def make_line_no_mo(judge):
    judge = judge.replace('lord', '')
    judge = judge.replace('lady', '')
    judge = judge.strip('\"')
    judge = judge.strip()
    line = ' \"' + judge + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#{}"]; \n'.format(judge.strip('\"'))
    return line 

def make_nodes(dot_file):
    if(bool(c.mo_judges)):
        for judge in c.all_judges:
            line = make_line_mo(judge)
            dot_file = dot_file + line
    else:
        for judge in c.all_judges:
            line = make_line_no_mo(judge)
            dot_file = dot_file + line
    return dot_file

def write_dot_file(dot_file, case_num):
    text_file = open("dot_files5/{}.dot".format(case_num), "w")
    text_file.write(dot_file)
    text_file.close()

def create_dot_file(case_num): 
    dot_file = 'digraph {} {{ \n K=0.6 \n'.format(case_num)
    dot_file = make_edges(dot_file)
    dot_file = make_nodes(dot_file)
    if(all_flag):
        dot_file = dot_file + "all [shape=\"diamond\"];"
    dot_file = dot_file + "\n}"
    return dot_file

#  trimming the 'lord' or 'lady' from the judge 
def trim_judge(full_name):
    full_name = full_name.strip()
    if(' ' in full_name):
        full_name = full_name.split(' ')
        if(len(full_name) != 1):
            full_name = full_name[1] 
            return full_name
    else:
        if(full_name == 'all'):
            all_flag = True
            full_name = full_name
            return full_name

def get_judge_names(df):
    all_judges_temp = []
    for i, row in df.iterrows():
        if('lord' in row.loc['from_col'] or 'lady' in row.loc['from_col']):
            judge = trim_judge(row.loc['from_col'])
            if(judge not in all_judges_temp):
                all_judges_temp.append(judge)
    return all_judges_temp

def check_mo(row):
    if('NAN' not in row.loc['mj_col']):
        mo = row.loc['mj_col']
        mo = mo.split(',')
        for m in mo:
            m = m.title()
            c.mo_judges.append(m)
        return mo

def populate_dict(row):
    this_dict = { 'from': row.loc['from_col'], 
            'to': row.loc['to_col'],
            'relation': row.loc['relation_col'],
            'line_number': row.loc['line_col']
    } 
    dict_copy = this_dict.copy()
    c.judge_dict.append(dict_copy)
    return c.judge_dict

def line_check(row):
    if 'fullagr' in row.loc['relation_col']:
        return True
    if 'partagr' in row.loc['relation_col']:
        return True
    if 'fulldis' in row.loc['relation_col']:
        return True
    if 'partdis' in row.loc['relation_col']:
        return True
    if 'outcome' in row.loc['relation_col']:
        return True
    else:
        return False

def get_rels(row):
    if line_check(row):
        c.judge_dict = populate_dict(row)
    return c.judge_dict

def iterate_rows(df):
    for i, row in df.iterrows():
        c.judge_dict = get_rels(row)
    return c.judge_dict

def parse_file(df):
    c.all_judges = get_judge_names(df)
    c.mo_judges = check_mo(df.iloc[0])
    c.judge_dict = iterate_rows(df) 
    return c.judge_dict

def make_graph(df, case_num):
    global all_flag
    all_flag = False
    c.judge_dict = parse_file(df)
    c.pass_judge_dict = c.judge_dict
    dot_file = create_dot_file(case_num)
    write_dot_file(dot_file, case_num)