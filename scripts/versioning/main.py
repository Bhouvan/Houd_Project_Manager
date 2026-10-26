import hou
import os
from utility_scripts import main as utils


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
    cache_name ='node.parm("cache_name").eval()'

    directory = 'hou.getenv("CACHE_PATH")'

    
    extension = 'hou.pwd().parmTuple("teststring")[hou.pwd().parm("extension").eval()]'
     

    cache_name='.'.join([cache_name,extension])
    
    list_file = directory.split('/')
    list_file.append(cache_name)
    
    cache_path = '/'.join(list_file)
    print(cache_path)
    # node.parm('cache_path').setExpression('"{0}/{1}"'.format(directory,cache_name),language = hou.exprLanguage.Python)
    
    # node.parm('cache_path').setExpression('"{0}"'.format(cache_path),language = hou.exprLanguage.Python)
    expr1 = '("/").join([hou.getenv("CACHE_PATH"),hou.pwd().parm("cache_name").eval()])'
    expr2 = 'hou.pwd().parmTuple("teststring")'
    expr3 = 'hou.pwd().parm("extension").eval()'
    expr4 = 'expr2[expr3].eval()'
    expr = '(".").join([expr1,expr2[expr3].eval()])'
    # return expr
    expr = 'expr1 = {expr1}\n' \
    'expr2 = {expr2}\n' \
    'expr3 = {expr3}\n' \
    'expr4 = {expr4}\n' \
    'expr = {expr}\n' \
    'print (expr)\n' \
    'return expr'.format(expr1=expr1,expr2=expr2,expr3=expr3,expr4=expr4,expr=expr) 
    node.parm('cache_path').setExpression(expr,language = hou.exprLanguage.Python)
    
    # node.parm('cache_path').lock('True')
    # print(cache_path)

def save_to_disk():
    print('saveed to disk message')
    
def save_in_background():
    print('save in background message')