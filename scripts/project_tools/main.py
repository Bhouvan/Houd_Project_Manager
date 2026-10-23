import hou
import os
import json
from utility_scripts import main as util

proj_list = 'D:/PythonHoud/Work/_Houdini_/config/proj_list.json'
def read_proj():
    try:
        with open(proj_list,'r') as f:
            data = json.load(f)
    except ValueError:
        data = {}
    return data

def write_proj():
    try:
        with open(proj_list,'w') as f:
            data = json.load(f)
    except ValueError:
        data = {}
    return data

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

def add_proj():
    data = read_proj()
    # init
    path = None
    proj_name = None
    proj_code = None
    proj_code = None

    repeat = True

    while repeat:
        repeat=not repeat
        _path=hou.ui.selectFile(title = 'select project directory',
                                file_type = hou.fileType.Directory)
        
        path = os.path.dirname(_path)
        if path == '':
            return

        for k,v in data.items():
            if util.fix_path(path) == util.fix_path(v['PATH'])         :
                repeat=not repeat
                message = 'Project path is already used by project {0}.\nPlease select a different path'.format(k)
                errormessage(message,hou.severityType.Error)
                break

        if repeat:
            continue
        _proj_name = os.path.split(path)[-1]

    repeat = True
    while repeat:
        repeat = not repeat 
        inputs = hou.ui.readMultiInput(message='Enter project Data', 
                            input_labels = ('Project Name','Project Code','Project FPS'),
                            buttons=('Ok','Cancel'),
                            initial_contents=(_proj_name,'','25'))

        if inputs[0]==1:
            return
        proj_name = inputs[1][0]
        proj_code = inputs[1][1]
        proj_fps = inputs[1][2]

        if proj_name=='' or proj_code=='' or proj_fps=='':
            repeat = not repeat
            message = 'Fill all the fieds'
            util.errormessage(message,hou.severityType.Error)
            continue

        try:
            int(proj_fps)
        except ValueError:
            message='FPS not set to a number.\nPlease enter a whole number'
            util.errormessage(message,hou.severityType.Error)
            repeat = not repeat
            continue

        for k,v in data.items():
            if fix_path(proj_name) == fix_path(k):
                repeat=not repeat
                message = 'Project name is already used by project {0}.\nPlease select a different name'.format(k)
                util.errormessage(message,hou.severityType.Error)
                break
            if fix_path(proj_code) == fix_path(v['CODE']):
                repeat=not repeat
                message = 'Project code is already used by project {0}.\nPlease use a different code'.format(k)
                util.errormessage(message,hou.severityType.Error)
                break
                    
        if(repeat):
            continue

    if proj_name and proj_code and proj_fps:
        proj_data = {
            'CODE':proj_code,
            'PATH':path,
            'FPS':proj_fps
        }
        data[proj_name] = proj_data

    if data:
        with open(proj_list,'w') as f:
            json.dump(data,f,sort_keys=True,indent = 4) 
def remove_proj():
    data = read_proj()
    projects = list(data.keys())
    # print(projects)
    sel = hou.ui.selectFromList(projects,
                          message='Select project to remove',
                          title = 'Remove Project',
                          column_header = 'Project',
                          clear_on_cancel= True)
    if len(sel)==0:
        return

    for i in sel:
        key = projects[i]
        print (key)
        del data[key]
        print('removed')

    
    
    with open(proj_list,'w') as f:
        json.dump(data,f,sort_keys=True,indent = 4) 

def details_proj():
    data = read_proj()
    projects = list(data.keys())
    # print(projects)
    sel = hou.ui.selectFromList(projects,
                        message='Select project',
                        title = 'Details Project',
                        column_header = 'Project',
                        clear_on_cancel= True)
    if len(sel)==0:
        return
    for i in sel:
        util.print_report('Project details','Name : {0}'.format(projects[i]),
        'Code : {0}'.format(data[projects[i]]['CODE']),
        'fps : {0}'.format(data[projects[i]]['FPS']),
        'path : {0}'.format(data[projects[i]]['PATH']))

                    

    

def print_report(header,*body):
    print('\n{header:=^50}'.format(header=header))
    for b in body:
        print('\t{0}'.format(b))

    print('='*50)

def manage_proj():
    sel = hou.ui.displayMessage('Select an action', buttons=('Add','Remove','Details','Cancel'))
    if sel==0:
        add_proj()
    elif sel==1:
        remove_proj()
    elif sel==2:
        details_proj()
    else:
        return