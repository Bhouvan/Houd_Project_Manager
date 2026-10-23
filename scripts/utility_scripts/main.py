import hou
import os
import json
import importlib

def fix_path(old_path,new_sep=('/')):
    _path = old_path.replace('\\','/')
    _path = _path.replace('\\\\','/')
    _path = _path.replace('//','/')
    if _path.endswith('/'):
        _path=_path[:-1]

    _path = _path.replace('/',new_sep)

    newpath = _path
    return newpath

def errormessage(message,severity = hou.severityType.Error):
    message = '{_severity} : {_message}'.format(_severity=severity.name(),_message=message)
    hou.ui.displayMessage (message, buttons = ('Ok',),severity=severity)

def Load(module):
    importlib.reload(module)  

def print_report(header,*body):
    print('\n{header:=^50}'.format(header=header))
    for b in body:
        print('\t{0}'.format(b))

    print('='*50)


def errormessage(message,severity = hou.severityType.Error):
    message = '{_severity} : {_message}'.format(_severity=severity.name(),_message=message)
    hou.ui.displayMessage (message, buttons = ('Ok',),severity=severity)