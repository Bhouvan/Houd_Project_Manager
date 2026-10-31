import hou
import os
import json
from utility_scripts import main as utils

cache_list = "D:/PythonHoud/Work/_Houdini_/config/cache_list.json"

def setFrameRange(kwargs):
    node = kwargs['node']
    vers = node.parm('frame_range').eval()
    
    if (vers==1):
        node.parm('f_rgx').setExpression('hou.playbar.frameRange()[0]',language =hou.exprLanguage.Python)
        node.parm('f_rgy').setExpression('hou.playbar.frameRange()[1]',language =hou.exprLanguage.Python)
        node.parm('f_rgz').setExpression('1',language =hou.exprLanguage.Python)
        

def onCreated(kwargs):
    node = kwargs['node']
    node.parm('cache_name').setExpression('hou.pwd().name()',language = hou.exprLanguage.Python)
    setPathCache(kwargs)
    
def setPathCache(kwargs):
    node = kwargs['node']
    # node.parm('cache_path').setExpression('"{0}"'.format(cache_path),language = hou.exprLanguage.Python)
    expr1 = '("/").join([hou.getenv("CACHE_PATH"),hou.pwd().parm("cache_name").eval()])'
    expr2 = 'hou.pwd().parmTuple("teststring")'
    expr3 = 'hou.pwd().parm("extension").eval()'
    expr4 = 'expr2[expr3].eval()'
    expr = '(".").join([expr1,expr2[expr3].eval()])'

    
    expr = 'expr1 = {expr1}\n' \
    'expr2 = {expr2}\n' \
    'expr3 = {expr3}\n' \
    'expr4 = {expr4}\n' \
    'expr = {expr}\n' \
    'return expr'.format(expr1=expr1,expr2=expr2,expr3=expr3,expr4=expr4,expr=expr) 
    node.parm('cache_path').setExpression(expr,language = hou.exprLanguage.Python)
    
def save_to_disk(kwargs):
    node = kwargs['node']
    enable_vers = node.parm('enable_vers') 
    data = None
    try:
        with open(cache_list,'r') as f:
            data =json.load(f)
    except ValueError:
        data = {}
    

    vers = None
    if(len(list(data.keys()))!=0):
        vers = "001"
        print('data not empty')
    else:
        print('data empty')
        vers = ""
    if(enable_vers):
        print (vers)

    print('saveed to disk message 2')
    
def save_in_background():
    print('save in background message')