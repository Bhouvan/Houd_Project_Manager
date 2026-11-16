import hou
import os
import json
from utility_scripts import main as utils

cache_list = "D:/PythonHoud/Work/_Houdini_/config/cache_list.json"
project_name = hou.getenv('PROJECT')
scene_name = hou.getenv('SCENE')
def open_cache_list():
    try:
        with open(cache_list,'r') as f:
            data =json.load(f)
    except ValueError:
        data = {}
    return data

def setFrameRange(kwargs):
    node = kwargs['node']
    vers = node.parm('frame_range').eval()
    
    if (vers==1):
        node.parm('f_rgx').setExpression('hou.playbar.frameRange()[0]',language = hou.exprLanguage.Python)
        node.parm('f_rgy').setExpression('hou.playbar.frameRange()[1]',language = hou.exprLanguage.Python)
        node.parm('f_rgz').setExpression('1',language =hou.exprLanguage.Python)
        

def onCreated(kwargs):
    node = kwargs['node']
    node.parm('cache_name').setExpression('hou.pwd().name()',language = hou.exprLanguage.Python)
    setPathCache(kwargs)
    
def setPathCache(kwargs):
    node = kwargs['node']
    enable_vers = node.parm('enable_vers').eval()
    
    vers = None
    current_proj = None
    current_scene = None
    data = open_cache_list()
    if (len(list(data.keys()))!=0):
        if data.get(project_name):
            current_proj = data[project_name]
          
            
            if current_proj.get(scene_name):
                current_scene = current_proj[scene_name]


        if (current_scene != None):
            if(len(current_scene)!=0):
            
                if(current_scene.get(node.path())):
                    vers = current_scene.get(node.path())[-1].get('vers')
                    print (vers)
                    setPath(node,vers)
                else:
                    vers = None
                    print ("The name of the node has changed cannot set the version")
                 
            else:
                vers = 1
                setPath(node,vers)
        else:
            vers = 1
            setPath(node,vers)
    else:
        vers = 1
        print('version is being set')
    
def save_to_disk(kwargs):
    node = kwargs['node']
    current_scene = None
    enable_vers = node.parm('enable_vers').eval()
    auto_vers = node.parm('auto_vers').eval()

   
    
    data = open_cache_list()
    if data.get(project_name):
            current_proj = data[project_name]
            if current_proj.get(scene_name):
                current_scene = current_proj[scene_name]
    
    vers = None
    
    if(enable_vers):

        if(auto_vers):

            if (current_scene != None and len(current_scene)!=0): 

                print(current_scene)
                if(current_scene.get(node.path())):
                    vers = current_scene.get(node.path())[-1].get('vers')
                    print(vers+1)
                    vers = vers+1
                    
                    
                else:
                    vers = 1
        else:
            
            vers = current_scene.get(node.path())[-1].get('vers')

    parms = {}
    hip = hou.hipFile.name()
    tobesaved = {"vers":vers,"hip":hip,"parms":parms}
    print(data)
    data[project_name][scene_name][node.path()].append(tobesaved)
    
    with open(cache_list,'w') as f:
        json.dump(data,f,sort_keys=True,indent = 4) 
   
    print('saved to disk message 2')
    print(getKeys(project_name,scene_name,node.path(),8))

def save_in_background():
    print('save in background message')

def setPath(node,vers):
    if(hou.getenv("CACHE_PATH")!= None and node.parm("cache_name").eval()!=None):
        expr1 = ("/").join([hou.getenv("CACHE_PATH"),node.parm("cache_name").eval()])
        
        if(vers!=None):
            expr1 = ("_").join([("_").join([expr1,'v{0:0>3}'.format(str(vers))]),''])

        expr2 = node.parmTuple("teststring")#this parmTuple is hidden on the hda. Look ->
        # -> Through the invisible parameter type properties of the HDA!

        expr3 = node.parm("extension").eval()
        expr4 = expr2[expr3].eval()
        expr5 = (".").join([expr1,expr4])
        node.parm('cache_path').setExpression('"{expr5}"'.format(expr5=expr5),language = hou.exprLanguage.Python)
    else:
        node.parm('cache_path').setExpression("'Project or scene not set'",language = hou.exprLanguage.Python)

   

def getKeys(project_name, scene_name, node_path, version = -1):

    dict = None
    data = open_cache_list()
    if(project_name != None and scene_name != None and node_path != None ):
        temp_dict = data[project_name][scene_name][node_path]
        if(len(temp_dict)!=0 and version < len(temp_dict)):
            dict = temp_dict[version]
        else: 
            print('index out of bound')
            return
        
    return dict