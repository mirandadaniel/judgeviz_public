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
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField
from wtforms import RadioField
from mysql.connector import Error
from string import ascii_lowercase
import re
import warnings
import codecs
import pydot
import make_mini_graphs  as mm
import make_tabs as mt
import metadata_scraper as ms
import make_graph_and_summary as mgs
from IPython.display import display
warnings.filterwarnings("ignore")

def highlight_roles(row):
    value = row.loc['role']
    color = ''
    if value == 'FACT' and 'fact' in selected_roles_list:
        color = '#deb6f0' 
    elif value == 'FRAMING' and 'framing' in selected_roles_list:
        color = '#bce0f7'
    elif value == 'TEXTUAL' and 'textual' in selected_roles_list:
        color = '#fcdef9'
    elif value == 'BACKGROUND' and 'background' in selected_roles_list:
        color = '#fcfcb1'
    elif value == 'PROCEEDINGS' and 'proceedings' in selected_roles_list:
        color = '#f2bf49'
    elif value == 'DISPOSAL' and 'disposal' in selected_roles_list:
        color = '#b9fabb'
    else:
        color = ''
    return ['background-color: {}'.format(color) for r in row]


def make_styled_table(df, selected_roles):
    global selected_roles_list 
    selected_roles_list = selected_roles
    styled_table = df.style.apply(highlight_roles, axis=1).hide([('case_id'), ('asmo'), ('asmo_sent_id'), ('sentence_id'), ('para_id'), ('judge'), ('role'), ('align'), ('agree'), ('outcome'), ('ackn'), ('provision_ent'), ('instrument_ent'), ('court_ent'), ('case_name_ent'), ('citation_bl_ent'), ('judge_ent'), ('title'), ('date'), ('house')], axis="columns").hide_columns()
    return styled_table


def remove_irrelevant_sentences(df, selected_roles_list):
    for i, row in df.iterrows():
        value = row.loc['role']
        judge_name_check = row.loc['case_text']
        if('LORD' in judge_name_check or 'LADY' in judge_name_check):
            print(f"{row}\n")
        else:
            if value == 'FACT' and 'fact' not in selected_roles_list:
                df.drop(i, axis=0, inplace=True)
            elif value == 'FRAMING' and 'framing' not in selected_roles_list:
                df.drop(i, axis=0, inplace=True)
            elif value == 'TEXTUAL' and 'textual' not in selected_roles_list:
                df.drop(i, axis=0, inplace=True)
            elif value == 'BACKGROUND' and 'background' not in selected_roles_list:
                df.drop(i, axis=0, inplace=True)
            elif value == 'PROCEEDINGS' and 'proceedings' not in selected_roles_list:
                df.drop(i, axis=0, inplace=True)
            elif value == 'DISPOSAL' and 'disposal' not in selected_roles_list:
                df.drop(i, axis=0, inplace=True)  
    return df
