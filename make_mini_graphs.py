from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import mysql.connector as mysql
from flask_cors import CORS
import numpy as np
import pandas as pd
import pydot
import os
import matplotlib.pyplot as plt
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
import pydot
import itertools
import config as c
warnings.filterwarnings("ignore")

import glob

global mo_flag 
global all_flag2

all_flag2 = False
mo_flag = False 


def strip_title(judge):
    if(' ' in judge):
        judge = judge.split(' ')
        judge = '\"' + judge[1] + '\"'
        return judge
    else:
        judge = judge
        return judge

def make_fullagr_edge(data, val):
    if(data[2] == 'all'):
        all_flag2 == True
    line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="darkgreen", arrowhead="normal", penwidth=1, href=\"#{}\"];'.format(val), '\n'
    line = ' '.join(line)
    line = ' ' + line
    return line

def make_partagr_edge(data, val):
    if(data[2] == 'all'):
        all_flag2 == True
    line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="darkgreen", arrowhead="onormal", penwidth=1, href=\"#{}\"];'.format(val), '\n'
    line = ' '.join(line)
    line = ' ' + line
    return line

def make_fulldis_edge(data, val):
    if(data[2] == 'all'):
        all_flag2 == True
    line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="red", arrowhead="dot", penwidth=1, href=\"#{}\"];'.format(val), '\n'
    line = ' '.join(line)
    line = ' ' + line
    return line

def make_partdis_edge(data, val):
    if(data[2] == 'all'):
        all_flag2 == True
    line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="red", arrowhead="odot", penwidth=1, href=\"#{}\"];'.format(val), '\n'
    line = ' '.join(line)
    line = ' ' + line
    return line

def make_outcome_edge(data, val):
    if(data[2] == 'all'):
            all_flag2 == True
    if(data[2] == 'self'):
        line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="blue", arrowhead="vee", penwidth=1, href=\"#{}\"];'.format(val), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line
    else:
        line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="blue", arrowhead="vee", penwidth=1, href=\"#{}\"];'.format(val), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line

def make_factagr_edge(data, val):
    if(data[2] == 'all'):
            all_flag2 == True
    if(data[2] == 'self'):
        line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="grey", arrowhead="normal", penwidth=1, href=\"#{}\"];'.format(val), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line
    else:
        line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="grey", arrowhead="normal", penwidth=1, href=\"#{}\"];'.format(val), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line

def make_ackn_edge(data, val):
    if(data[2] == 'all'):
            all_flag2 == True
    if(data[2] == 'self'):
        line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="yellow", arrowhead="normal", penwidth=1, href=\"#{}\"];'.format(val), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line
    else:
        line = '\"' + data[1] + '\"', '->', '{', '\"' + data[2] + '\"', '}', '[color="yellow", arrowhead="normal", penwidth=1, href=\"#{}\"];'.format(val), '\n'
        line = ' '.join(line)
        line = ' ' + line
        return line

def add_edge(data, val):
    rel = data[0]
    if(rel == 'fullagr'):
        edge = make_fullagr_edge(data, val)
        return edge
    if(rel == 'partagr'):
        edge = make_partagr_edge(data, val)
        return edge
    if(rel == 'fulldisa'):
        edge = make_fulldis_edge(data, val)
        return edge
    if(rel == 'partdisa'):
        edge = make_partdis_edge(data, val)
        return edge
    if(rel == 'outcome'):
        edge = make_outcome_edge(data, val)
        return edge
    if(rel == 'factagr'):
        edge = make_factagr_edge(data, val)
        return edge
    if(rel == 'ackn'):
        edge = make_ackn_edge(data, val)
        return edge

def make_edges(dot_file, data, values): 
    for val in values:
        edge = add_edge(data, val)
        dot_file = dot_file + edge
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

def make_nodes(dot_file, data, values):
    temp_mo = c.mo_judges
    mo_judges = []
    if(temp_mo is not None):
        for judge in temp_mo:
            judge = trim_judge(judge)
            mo_judges.append(judge)
    if 'self' in data[2]:
        data[2] = data[1]
    if(bool(mo_judges)):
        if(data[1] in mo_judges):
            line = ' \"' + data[1] + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="yellow", href=\"#{}\"]; \n'.format(data[1])
            dot_file = dot_file + line
        else:
            line = ' \"' + data[1] + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href=\"#{}\"]; \n'.format(data[1])
            dot_file = dot_file + line
        if(data[2] in mo_judges):
            line = ' \"' + data[2] + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="yellow", href=\"#{}\"]; \n'.format(data[2])
            dot_file = dot_file + line
        else:
            line = ' \"' + data[2] + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href=\"#{}\"]; \n'.format(data[2])
            dot_file = dot_file + line
    else:
        line = ' \"' + data[1] + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#{}"]; \n'.format(data[1])
        dot_file = dot_file + line
        line = ' \"' + data[2] + '\" [shape="circle", fixedsize="true", height=1, width=1, style="filled", fillcolor="white", href="#{}"]; \n'.format(data[2])
        dot_file = dot_file + line
    return dot_file

def edit_map(map_file, map_name):
    new_map_file = ''
    map_file = map_file.split('\n')
    for line in map_file:
        if('href="fullagr' in line or 'href="partagr' in line or 'href="fulldisa' in line or 'href="partdisa' in line or 'href="outcome' in line):
            line = line.replace('href', 'alt')
            line = line.replace('alt=\"\"', '')
            line_temp = line.split('/>')
            line = line_temp[0] + ' onclick="myFunction2(this.alt)"/>' 
            new_map_file =  new_map_file + line + '\n'
        elif('href' in line):
            line = line.replace('alt=\"\"', 'alt=\"{}\"'.format(map_name))
            line_temp = line.split('/>')
            line = line_temp[0] + ' onclick="return myFunction(this.alt, href);"/>' 
        new_map_file =  new_map_file + line + '\n'
    return new_map_file


def edit_mini_graph(map_name):
    with open('static/{}.map'.format(map_name),'r') as file:
        map_file = file.read()
    file.close()
    map_file = edit_map(map_file, map_name)
    text_file = open("static/{}.map".format(map_name), "w")
    text_file.write(map_file)
    text_file.close()


def make_new_graph(key, values):
    data = key.split('_')
    graph_name = key
    if('-' in graph_name):
        graph_name = graph_name.replace('-','')
    dot_file = 'digraph {} {{ \n K=0.6 \n'.format(graph_name)
    dot_file = make_edges(dot_file, data, values)
    dot_file = make_nodes(dot_file, data, values)
    if(all_flag2):
        dot_file = dot_file + "all [shape=\"diamond\"];"
    dot_file = dot_file + "\n}"
    text_file = open("temp_dot_files/{}.dot".format(graph_name), "w")
    text_file.write(dot_file)
    text_file.close()
    os.system("dot temp_dot_files/{}.dot -Tpng -o static/{}.png -Tcmapx -o static/{}.map".format(graph_name, graph_name, graph_name))
    edit_mini_graph(graph_name)

def make_judge_collections(judge_dict, all_judges):
    prev_from = ' '
    prev_to = ' '
    prev_relation = ' '
    d_of_collections = {}
    max  = len(judge_dict)
    for index, d in enumerate(judge_dict):
        temp = []
        fromj = d['from'].split()
        fromj = fromj[1]
        if('self' not in d['to'] and 'all' not in d['to']):
            to = d['to'].split()
            to = to[1]
        else: 
            to = d['to']
        collection_name = d['relation'] + '_' + fromj + '_' + to
        if(d['from'] == prev_from and d['to'] == prev_to and d['relation'] == prev_relation):
            if(collection_name not in d_of_collections):
                d_of_collections[collection_name] = []
                list_to_insert  = [d['line_number']]
                d_of_collections[collection_name].extend(list_to_insert)
            else:
                list_to_insert  = [d['line_number']]
                d_of_collections[collection_name].extend(list_to_insert)
        else:
            if(collection_name not in d_of_collections):
                d_of_collections[collection_name] = []
                list_to_insert  = [d['line_number']]
                d_of_collections[collection_name].extend(list_to_insert)
            else:
                list_to_insert  = [d['line_number']]
                d_of_collections[collection_name].extend(list_to_insert)
            prev_from = d['from']
            prev_to = d['to']
            prev_relation = d['relation']
    return d_of_collections

def make_smaller_graphs(judge_dict, all_judges, all_mini_files):
    judge_collections = make_judge_collections(judge_dict, all_judges)
    key_list = list(judge_collections.keys())
    for file in all_mini_files:
        for key in key_list:
            if(key == file):
                if('-' in key):
                    key.replace('-', '')
                values = judge_collections[key]
                make_new_graph(key, values)
                

    