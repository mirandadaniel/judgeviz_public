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
import itertools
warnings.filterwarnings("ignore")

def make_content(name):
    line = '<div id="{}" class="tabcontent">\n'.format(name) 
    line = line + '<h6> This arrow represents multiple arrows: </h6>\n'
    line = line + '<img src="/static/{}.png" usemap="#{}"/>\n'.format(name, name)
    file = 'static/{}.map'.format(name)
    with open(file,'r') as file:
        map_file = file.read()
    file.close()
    line = line + map_file + '</div>\n'
    return line

def make_button(name):
    line = '<button class="tablinks" onclick="openTab(event, \'{}\')"></button>\n'.format(name)
    return line

def make_html_file(all_mini_files):
    global html_file
    html_file = '<div class="tab">\n'
    for file in all_mini_files:
        line = make_button(file)
        html_file = html_file + line
    html_file = html_file + '<button class="tablinks" onclick="openTab(event, \'blank\')"></button>\n'
    for file in all_mini_files:
        line = make_content(file)
        html_file = html_file + line
    line = '<div id="blank" class="tabcontent">\n</div>'
    html_file = html_file + line 
    html_file = html_file + '</div>\n'
    file = open("static/tab_file.html","w")
    file.write(html_file)
    file.close()    
    
