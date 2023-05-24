from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import mysql.connector as mysql
# import numpy as np
# import pandas as pd
import pydot
import os
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField
from wtforms import RadioField
from mysql.connector import Error
from string import ascii_lowercase
import re

global mo_flag
mo_flag = False

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = ""
)
# print(db)

def trim_judge(full_name):
    full_name = full_name.split(' ')
    if(len(full_name) != 1):
        full_name = '\"' + full_name[1] + '\"'
        return full_name
    else:
        if(full_name == 'all'):
            all_flag = True
            return full_name[0]
        else:
            return full_name[0]

def check_part_agr(line):
    if('partagr' in line[5]):
        judge_from = trim_judge(line[3])
        judge_to = trim_judge(line[4])
        if(judge_to == 'self'):
            judge_to = judge_from
        if(judge_from not in pa_judges):
            pa_judges[judge_from] = []
            pa_judges[judge_from].append(judge_to)
        else: 
            pa_judges[judge_from].append(judge_to)

def check_full_agr(line):
    if('fullagr' in line[5]):
        judge_from = trim_judge(line[3])
        judge_to = trim_judge(line[4])
        if(judge_to == 'self'):
            judge_to = judge_from
        if(judge_from not in fa_judges):
            fa_judges[judge_from] = []
            fa_judges[judge_from].append(judge_to)

        else: 
            fa_judges[judge_from].append(judge_to)

def check_part_disagr(line):
    if('partdisa' in line[5]):
        judge_from = trim_judge(line[3])
        judge_to = trim_judge(line[4])
        if(judge_to == 'self'):
            judge_to = judge_from
        if(judge_from not in pd_judges):
            pd_judges[judge_from] = []
            pd_judges[judge_from].append(judge_to)
        else: 
            pd_judges[judge_from].append(judge_to)

def check_full_disagr(line):
    if('fulldisa' in line[5]):
        judge_from = trim_judge(line[3])
        judge_to = trim_judge(line[4])
        if(judge_to == 'self'):
            judge_to = judge_from
        if(judge_from not in fd_judges):
            fd_judges[judge_from] = []
            fd_judges[judge_from].append(judge_to)
        else: 
            fd_judges[judge_from].append(judge_to)

def check_outcomes(line):
    if('outcome' in line[5]):
        judge_from = trim_judge(line[3])
        judge_to = trim_judge(line[4])
        if(judge_to == 'self'):
            judge_to = judge_from
        if(judge_from not in outcomes):
            outcomes[judge_from] = []
            outcomes[judge_from].append(judge_to)
        else: 
            outcomes[judge_from].append(judge_to)

def check_mo(line):
    if('NAN' not in line[7]):
        mo = line[7].split(',')
        return mo



def parse_file(file):
    global fa_judges
    global pa_judges
    global fd_judges
    global pd_judges
    global outcomes
    global mo_judges
    fa_judges = {}
    pa_judges = {}
    fd_judges = {}
    pd_judges = {}
    outcomes = {}
    mo_judges = []
    with open('/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz2/graph_files/{}'.format(filename), 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split('\t')
        if(line[1] == '0'):
            mo_judges = check_mo(line)
        else:
            check_full_agr(line)
            check_part_agr(line)
            check_full_disagr(line)
            check_part_disagr(line)
            check_outcomes(line)
    f.close()

def populate_fa(dot_file):
    for key in fa_judges:
        judges_to = ' '.join(fa_judges[key])
        line = ' ' + key, '->', '{', judges_to, '}', '[color="darkgreen"]', '\n'
        line = ' '.join(line)
        dot_file = dot_file + line
    return dot_file

def populate_pa(dot_file):
    for key in pa_judges:
        judges_to = ' '.join(pa_judges[key])
        line = ' ' + key, '->', '{', judges_to, '}', '[color="darkgreen", style="dotted"]' '\n'
        line = ' '.join(line)
        dot_file = dot_file + line
    return dot_file

def populate_fd(dot_file):
    for key in fd_judges:
        judges_to = ' '.join(fd_judges[key])
        line = ' ' + key, '->', '{', judges_to, '}', '[color="red", arrowhead="dot"]' '\n'
        line = ' '.join(line)
        dot_file = dot_file + line
    return dot_file

def populate_pd(dot_file):
    for key in pd_judges:
        judges_to = ' '.join(pd_judges[key])
        line = ' ' + key, '->', '{', judges_to, '}', '[color="red", style="dotted", arrowhead="dot"]' '\n'
        line = ' '.join(line)
        dot_file = dot_file + line
    return dot_file

def populate_outcomes(dot_file):
    for key in outcomes:
        judges_to = ' '.join(outcomes[key])
        line = ' ' + key, '->', '{', judges_to, '}', '[color="blue"]' '\n'
        line = ' '.join(line)
        dot_file = dot_file + line
    return dot_file

def populate_mo(dot_file):
    if(bool(mo_judges)):
        for judge in mo_judges:
            judge = judge.replace('lord', '')
            judge = judge.strip()
            judge = '\"' + judge + '\"'
            line = ' ' + judge + ' [style="filled", fillcolor="yellow"] \n'
            dot_file = dot_file + line
        return dot_file
    return dot_file

def create_dot_file(): 
    global dot_file
    dot_file = 'digraph case{} {{ \n K=0.6 \n'.format(case_num)
    dot_file = populate_fa(dot_file)
    dot_file = populate_pa(dot_file)
    dot_file = populate_fd(dot_file)
    dot_file = populate_pd(dot_file)
    dot_file = populate_outcomes(dot_file)
    dot_file = populate_mo(dot_file)
    if(all_flag):
        dot_file = dot_file + " all [shape=\"diamond\"]\n}"
    else:
        dot_file = dot_file + "\n}"
    text_file = open("dot_files3/{}.dot".format(filename_without), "w")
    text_file.write(dot_file)
    text_file.close()

global all_flag
global filename
global filename_without 
global file_x
global case_num

all_flag = False

directory = os.fsencode('/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz3/graph_files')
for file in os.listdir(directory):
    file_x = file

    filename = os.fsdecode(file)
    if filename.endswith(".tsv") and filename == 'case6.tsv': 
        filename_arr = filename.split(".")
        filename_without = filename_arr[0]
        word = 'case'
        case_num = filename_arr[0].replace(word, "")
        parse_file(file_x)
        create_dot_file()
        continue
    else:
        continue