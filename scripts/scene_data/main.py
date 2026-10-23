import hou
import sys
import json
import os
from utility_scripts import main as util
proj_list ='D:/PythonHoud/Work/_Houdini_/config/proj_list.json' 

def read_json():
    try:
        with open(proj_list,'r') as f:
            data = json.load(f)
    except ValueError:
        data = {}

    return data

def create_folder_and_var(var,path):
    path = util.fix_path(path)
    hou.putenv(var,path)

    if not os.access(path,os.F_OK):
        os.makedirs(path)
        print('creating folder {0} [{1}]'.format(var,path))

def scene_menu(kwargs):
    menu = []   
    scenes_path = hou.getenv('SCENES_PATH')
    if scenes_path and os.access(scenes_path,os.F_OK):
        for f in os.listdir(scenes_path):
            if os.path.isdir(util.fix_path(os.path.join(scenes_path,f))):
                menu.append(f)
                menu.append(f)
    return menu

        

def project_menu(kwargs):
    data = read_json()
    menu = ['-','-']
    for k in data.keys():
        menu.append(k)
        menu.append(k)

    return menu
def set_project(kwargs):
    node = kwargs['node']
    # project_name = node.evalParm('proj')
    project_name = kwargs['script_value']
    # reset scene to none
    node.parm('scene').set('')
    unset_scene('',node)

    data =read_json()

    if project_name=='-':
        hou.unsetenv('PROJECT')
        hou.unsetenv('CODE')
        hou.unsetenv('PROJ_FPS')
        hou.unsetenv('PROJ_PATH')
        hou.unsetenv('SCENES_PATH')
        hou.unsetenv('HDA_PATH')
        hou.unsetenv('SCRIPTS_PATH')
        node.cook(True)
        return

    try:
        project_data = data[project_name]
    except KeyError:
        util.errormessage('Project data notfound')
        return

    hou.putenv('PROJECT',project_name)
    hou.putenv('CODE',project_data['CODE'])
    fps = project_data['FPS']
    hou.putenv('PROJ_FPS',fps)
    hou.setFps(int(fps))
    project_path = project_data['PATH']
    hou.putenv('PROJ_PATH',project_path)
    create_folder_and_var('SCENES_PATH',util.fix_path(os.path.join(project_path,'scenes')))
    hda_path = util.fix_path(os.path.join(project_path,'hda'))
    create_folder_and_var('HDA_PATH',hda_path)
    scripts_path = util.fix_path(os.path.join(project_path,'scripts'))
    create_folder_and_var('SCRIPTS_PATH',scripts_path)
    # scan_path = hou.getenv('HOUDINI_OTLSCAN_PATH')

    # hda_paths = [hda_path,]
    # if scan_path :
    #     hda_paths +=scan_path.split(';')
    # hda_paths=list(set(hda_paths))

    # hou.putenv('HOUDINI_OTLSCAN_PATH',';'.join(hda_paths))
    hou.hda.reloadAllFiles()

    sys.path.append(scripts_path)
    node.cook(True)

def set_scene(kwargs):
    node = kwargs['node']
    scene_name = node.evalParm('scene')
    if unset_scene(scene_name,node):
        return
    # if null scene then unset all

    # if no PROJECT_PATH var

    project_path = hou.getenv('PROJ_PATH')
    if not project_path or not os.access(project_path,os.F_OK):
        util.errormessage('Project path is invalid')
        return
    # if no SCENES_PATH var
    scenes_path = hou.getenv('SCENES_PATH')
    if not scenes_path:
        util.errormessage('Scene path is invalid')
        return
    #if SCENE_PATH var but no folder
    if not os.access(scenes_path,os.F_OK):
        os.makedirs(scenes_path)

    scene_path = util.fix_path(os.path.join(scenes_path,scene_name))

    if not os.access(scene_path,os.F_OK):
        message = 'Scene folder "{0}" does not exist\n'\
            'Create this folder now ?'.format(scene_name)
        choice = hou.ui.displayMessage(message,severity=hou.severityType.ImportantMessage,buttons = ('Yes','No'))

        if choice==0:
            os.makedirs(scene_path)
        else:
            unset_scene('',node)
            node.parm('scene').set('')
            return
           


    hou.putenv('SCENE',scene_name)
    hou.putenv('SCENE_PATH',scene_path)
    create_folder_and_var('SAVE_PATH',os.path.join(scene_path,'working_files'))

    output_path = os.path.join(scene_path,'output')
    create_folder_and_var('OUTPUT_PATH',output_path)
    create_folder_and_var('CACHE_PATH',os.path.join(output_path,'cache'))
    create_folder_and_var('RENDER_PATH',os.path.join(output_path,'render'))
        
    node.cook(True)


def unset_scene(scene,node):
     quit = False
     if(scene==''):
        hou.unsetenv('SCENE')
        hou.unsetenv('SCENE_PATH')
        hou.unsetenv('SAVE_PATH')
        hou.unsetenv('OUTPUT_PATH')
        hou.unsetenv('CACHE_PATH')
        hou.unsetenv('RENDER_PATH')
        node.cook(True)
        quit = not quit
        return quit
def onLoaded(kwargs):
    node = kwargs['node']
    curr_scene = node.evalParm('scene')
    print (curr_scene)
    node.parm('project').pressButton()
    
    if not curr_scene == '':
        if curr_scene in scene_menu({}):
            node.parm('scene').set(curr_scene)
            node.parm('scene').pressButton()
        else:
            node.parm('scene').set('')

def onCreated(kwargs):
    node = kwargs['node']
    node.setName('SCENE_DATA')
    node.setUserData('nodeshape','circle')
    node.setColor(hou.Color(0.58,0.2,0.48))
    node.setGenericFlag(hou.nodeFlag.Display,False)
    node.setGenericFlag(hou.nodeFlag.Selectable,False)
    if(hou.getenv('PROJECT')):
        node.parm('project').set(hou.getenv('PROJECT'))
    # else:
    #     node.parm('project').set('-')
    if(hou.getenv('SCENE')):
        node.parm('scene').set(hou.getenv('SCENE'))
    else:
        node.parm('scene').set('')