from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import mysql.connector as mysql
from flask_cors import CORS
import numpy as np
import pandas as pd
import pydot
import os
import cv2
import unittest
import pytest
from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField
from wtforms import RadioField
from mysql.connector import Error
from string import ascii_lowercase
import re
import warnings
import codecs
import make_graph as mg
import make_mini_graphs  as mm 
import make_tabs as mt
import metadata_scraper as ms
import make_graph_and_summary as mgs
import highlight_roles as hr
import format_dataframe as fd
import sshtunnel
from IPython.display import display
import config as c 
from sqlalchemy import create_engine
import pymysql


def reset_config():
    c.all_mini_files = []
    c.mo_flag = False 
    c.dictionary = {}
    c.dictionary = { 1000000 : 'nothing' }
    c.pass_judge_dict = ''
    c.all_judges = []
    c.outcomes = {}
    c.mo_judges = []
    c.judge_dict = []

dir_name = "/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/virtualEnv2/graphviz7/static/"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".png") or item.endswith(".map"):
        if("logo" not in item and "ex1" not in item and "expand" not in item and "hover" not in item):
            os.remove(os.path.join(dir_name, item))

SECRET_KEY = 'development'
app = Flask(__name__)
app.config.from_object(__name__)
cors = CORS(app)

sqlEngine       = create_engine('mysql+pymysql://root:@127.0.0.1/all_data', pool_recycle=3600)
dbConnection    = sqlEngine.connect()

def capitalize_double_barrelled(judge):
    judge = judge.split('-')
    judge = judge[0].capitalize() + '-' + judge[1].capitalize()
    return judge

def find_mo_judges():
    if(c.mo_judges is not None):
        total = len(c.mo_judges)
        count = 0
        if(total != 0):
            sentence = 'The majority opinion is given by '
            for judge in c.mo_judges:
                if("\"" in judge):
                    judge = judge.strip('"')
                if("-" in judge):
                    judge = capitalize_double_barrelled(judge)
                else:
                    judge = judge.title()
                sentence = sentence + judge
                count+=1
                if(count == total-1):
                    sentence = sentence + ' and '
                elif(count == total):
                    sentence = sentence + '.'
                    return sentence
                else: 
                    sentence = sentence + ', '
        else:
            return 'There is no majority opinion in this case.'
    else:
        return 'There is no majority opinion in this case.' 

def get_case_names():
    allowed_cases = ['case22', 'case23', 'case11', 'case12', 'case14', 'case13', 'case5', 'case20', 'case3', 'case2', 'case21', 'case7', 'case4', 'case15', 'case18', 'case19', 'case6', 'case17', 'case42', 'case38', 'case26', 'case45', 'case43', 'case31', 'case35', 'case36', 'case32', 'case40', 'case24', 'case34', 'case47', 'case69', 'case55', 'case57', 'case62', 'case46', 'case60', 'case49', 'case56', 'case66', 'case52']
    case_titles = []
    for x in allowed_cases:
        x = 'text_' + x
        df_2 = pd.read_sql('select title, house, date from all_data.' + x + ';', dbConnection)       
        title = df_2.iloc[0, 0]
        house = df_2.iloc[0, 1]
        date = df_2.iloc[0, 2]
        y = x.split('case')
        y = "Case " + y[1]
        case_data = y + ' : ' + title + ' (' + house + ') ' + date 
        case_titles.append(case_data) 
    return case_titles

def get_graph_case_names():
    allowed_cases = ['case40', 'case63', 'case69', 'case32', 'case23', 'case17', 'case47', 'case46', 'case62', 'case12', 'case53', 'case2', 'case34', 'case49', 'case38', 'case55', 'case66', 'case15', 'case45', 'case68', 'case21', 'case57', 'case29', 'case6', 'case42', 'case36']
    case_titles = []
    for x in allowed_cases:
        df_2 = pd.read_sql('select title, house, date from all_data.' + x + ';', dbConnection)      
        title = df_2.iloc[0, 0]
        house = df_2.iloc[0, 1]
        date = df_2.iloc[0, 2]
        y = x.split('case')
        y = "Case " + y[1]
        case_data = y + ' : ' + title + ' (' + house + ') ' + date 
        case_titles.append(case_data) 
    return case_titles

def check_mo(line):
    line_string = line
    line = line_string.strip()
    line = line.split(" ")
    mo_judges_temp = []
    if(len(line) > 1):
        if("fillcolor=\"yellow\"" in line_string):
            mo_judges_temp.append(line[0])
    return mo_judges_temp

def check_judge(line):
    if('shape="circle"' in line or 'shape="diamond"' in line):
        line = line.strip()
        line = line.split(" ")
        judges.append(line[0])

def parse_all_file(case_name):
    (graph, ) = pydot.graph_from_dot_file('dot_files5/{}.dot'.format(case_name))
    graph.write_png('static/case_x.png'.format(case_name))

def edit_map(map_file):
    new_map_file = ''
    map_file = map_file.split('\n')
    for line in map_file:
        if('href="fullagr' in line or 'href="partagr' in line or 'href="fulldisa' in line or 'href="partdisa' in line or 'href="outcome' in line):
            line = line.replace('href', 'alt')
            line = line.replace('alt=\"\"', '')
            line_temp = line.split('/>')
            line = line_temp[0] + ' onclick="return myFunction2(this.alt);"/>' 
            new_map_file =  new_map_file + line + '\n'
        elif('href' in line):
            line = line.replace('alt=\"\"', 'alt=\"blank\"')
            line_temp = line.split('/>')
            line = line_temp[0] + ' onclick="return myFunction(this.alt, href);"/>' 
        new_map_file =  new_map_file + line + '\n'
    return new_map_file

def highlight_all_rels(row):
    value = row.loc['relation_col']
    color = ''
    return ['background-color: {}'.format(color) for r in row]

def get_case_name(long_name):
    split = long_name.split(' ')
    case_name = split[0] + split[1]
    case_name = case_name.lower()
    return case_name

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SimpleForm(FlaskForm):
    string_of_files = ['fact\r\nbackground\r\nframing\r\ntextual\r\nproceedings\r\ndisposal\r\nhide irrelevant sentences']
    list_of_files = string_of_files[0].split('\r\n')
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)

class graphForm(FlaskForm):
    string_of_files = ['Full agreements\r\nPartial agreements\r\nFull disagreements\r\nPartial disagreements\r\nOutcomes']
    list_of_files = string_of_files[0].split('\r\n')
    files = [(x, x) for x in list_of_files]
    example = MultiCheckboxField('Label', choices=files)

class SelectionForm(FlaskForm):
    string_of_options = ['Graph and text\r\nGraph and summary\r\nSummary and text']
    list_of_options = string_of_options[0].split('\r\n')
    options = [(x, x) for x in list_of_options]
    example = RadioField('Label', choices=options)

class CaseForm(FlaskForm):
    string_of_cases = get_case_names()
    list_of_cases = string_of_cases 
    cases = [(x, x) for x in list_of_cases]
    example = RadioField('Label', choices=cases)

class GraphCaseForm(FlaskForm):
    string_of_cases = get_graph_case_names()
    list_of_cases = string_of_cases 
    cases = [(x, x) for x in list_of_cases]
    example = RadioField('Label', choices=cases)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/select_roles', methods=['GET', 'POST'])
def select_roles():
    table_case_name = 'text_' + case_name
    df = pd.read_sql('SELECT * FROM all_data.{}'.format(table_case_name), dbConnection) 
    form = SimpleForm()
    if form.validate_on_submit():
        selected_roles_list = form.example.data
        selected_roles = ' '.join(selected_roles_list)
        if('hide irrelevant sentences' in selected_roles):
            df = hr.remove_irrelevant_sentences(df, selected_roles_list)
            styled_table = hr.make_styled_table(df, selected_roles_list)
            return render_template('index.html',  tables=[styled_table.to_html(classes='data')], titles=df.columns.values)
        else:
            styled_table = hr.make_styled_table(df, selected_roles_list)
            return render_template('index.html',  tables=[styled_table.to_html(classes='data')], titles=df.columns.values)
    else:
        print("Validation Failed")
        print(form.errors)
    return render_template('example.html',form=form)


@app.route('/select_case', methods=['GET', 'POST'])
def select_case():
    form = CaseForm()
    if form.validate_on_submit():
        global case_name
        selected_case = form.example.data
        case_name = get_case_name(selected_case)
        return redirect('/select_roles')
    else:
        print("Validation Failed")
        print(form.errors)
    return render_template('choose_case.html', form=form) 

@app.route('/graph_select_case', methods=['GET', 'POST'])
def graph_select_case():
    form = GraphCaseForm()
    if form.validate_on_submit():
        global case_name
        global full_case_name
        selected_case = form.example.data
        full_case_name = selected_case
        case_name = get_case_name(selected_case)
        return redirect('/interactive_graph')
    else:
        print("Validation Failed")
        print(form.errors)
    return render_template('graph_choose_case.html', form=form) 

@app.route('/interactive_graph', methods=['GET', 'POST'])
def interactive_graph():
    reset_config()
    global judges
    judges = []
    mo_judges = []
    form = graphForm()
    df = pd.read_sql('SELECT * FROM all_data.{}'.format(case_name), dbConnection)
    temp_df = df
    temp_df2 = df
    mg.make_graph(df, case_name)
    gs_name = 'bbb' + case_name
    mg.create_dot_file(gs_name)
    mm.make_smaller_graphs(c.pass_judge_dict, c.all_judges, c.all_mini_files)
    parse_all_file(case_name) 
    judges = c.all_judges
    maj_op = find_mo_judges()
    os.system("dot dot_files5/{}.dot -Tpng -o static/case_x2.png -Tcmapx -o static/case_x2.map".format(case_name))
    title = full_case_name
    date_df = pd.read_sql('SELECT date FROM all_data.{}'.format(case_name), dbConnection)
    date = date_df.iloc[0]
    date = date_df['date'].iloc[0]
    df = fd.format_dataframe(df)
    temp_styled_table = df.style.apply(highlight_all_rels, axis=1).hide([('line_col'), ('case_num'), ('from_col'), ('to_col'), ('pos_col'), ('mj_col'), ('title'), ('house'), ('date')], axis="columns").hide_columns().hide_index()
    temp_styled_table.to_html('static/graph_text.html')
    fp= open('static/graph_text.html', 'a')
    fp.write('<br><br><br>')
    fp.close()
    ms.main(date, full_case_name, case_name, temp_df, dbConnection)
    with open('static/case_x2.map','r') as file:
        map_file = file.read()
    file.close()
    map_file_temp = map_file
    map_file = edit_map(map_file) 
    full_filename = '/Users/mirandadaniel/Documents/Comp_Sci/summer_project/PYTHON/graphviz7/static/case_x2.png'
    map_name = '#' + case_name
    mt.make_html_file(c.all_mini_files)
    mgs.make_summary(date, full_case_name, case_name, temp_df2, dbConnection)
    return render_template('graph_page.html', form=form, user_image=full_filename, map_name=map_name, map_file=map_file, case_name=full_case_name, maj_op=maj_op, judge1=judges[0].strip('"'), judge2=judges[1].strip('"'), judge3=judges[2].strip('"'), judge4=judges[3].strip('"'), judge5=judges[4].strip('"'))

@app.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('help.html')

@app.route('/study_info', methods=['GET', 'POST'])
def study_info():
    return render_template('study_info.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')

