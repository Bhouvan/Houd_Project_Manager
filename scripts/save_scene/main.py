import hou
import os
import re
from utility_scripts import main as utils

def clean_name(name):
    new_name = name.lower().strip()
    regex = r'\W+'
    new_name = re.sub(regex,'_',new_name)
    return new_name

def save_scene(kwargs=None,task=None,desc=None):
    ctrl = False
    if kwargs:
        ctrl = kwargs['ctrlclick']
    else:
        ctrl = False

    #find scene_data node
    scene_data = None
    scene_data_nodes = []
    for n in hou.node('/obj/').children():
        if n.type().nameComponents()[2].startswith('scene_data'):
            scene_data_nodes.append(n)
    
    if(len(scene_data_nodes)>1):
        utils.errormessage('Multiple Scene Data Found\nAborting Operation',hou.severityType.Error)
        return
    elif(len(scene_data_nodes)==1):
        scene_data = scene_data_nodes[0]
    else:
        utils.errormessage('No Scene Data Found\nPlease create one and select a scene before saving',hou.severityType.Error)
        return

    save_path = hou.getenv('SAVE_PATH')
    scene = hou.getenv('SCENE')

    if not save_path or not scene:
        utils.errormessage('Local variables not ddefined\nPlease use SCENE_DATA node to set scene correctly')
        return
    
    # Input Task and description from current scene or Initialize
    curr_name = hou.hipFile.basename()
    regex = r'^(?P<scene>\w+)-(?P<task>\w+)-(?P<full_ver>v(?P<ver>\d{3,}))(-(?P<desc>\w+))?-(?P<user>\w+)(\.(?P<ext>\w+))$'
    match = re.match(regex,curr_name,flags=re.I)
    if match:
        if not task:
            task = match.group('task')
        if not desc:
            desc = match.group('desc')
    if not task:
        task = ''
    if not desc:
        desc = ''

    ask_input = True 

    if ctrl and task!= '':
        ask_input = not ask_input
        
    # Input Task and description
    if ask_input:
        repeat = True
        while(repeat):
            repeat = not repeat
            user_input = hou.ui.readMultiInput('Select task and description',('Task','Description(Optional)'),buttons=('Ok','Cancel'),initial_contents=(task,desc))
            if user_input [0]==1:
                return
            task = user_input[1][0]

            desc = user_input[1][1]

            if task =='':
                utils.errormessage('Task can\'t be left blank',hou.severityType.Warning)
                repeat = not repeat 
                continue

    #set version
    regex = '(?P<scene>{scene})-(?P<task>{task})-v(?P<vers_num>\\d{{3,}})'.format(scene=scene,task=task)
    vers_nums = []
    for f in  os.listdir(save_path):
        if not os.path.isdir(f):
            match = re.match(regex,f,flags = re.IGNORECASE)#or re.I
            if match:
                vers_nums.append(int(match.group('vers_num')))


    if len(vers_nums)>0:
        high_vers = sorted(vers_nums)
        if(ctrl):
            ver = 'v{0:>03}'.format(high_vers[-1])
        else:
            ver = 'v{0:>03}'.format(high_vers[-1]+1)
        
    else:
        ver = 'v001'

    # set user_name
    user = hou.getenv('NAME').lower()

    components = [scene, task,ver,desc,user]
    for i,c in enumerate(components):
        if c and c!='':
            components[i]=clean_name(c)
        else:
            del components[i]

    # Set Extension
    lic_dict = {
        'Commercial':'hip',
        'Indie':'hiplc',
        'Apprentice':'hipnc',
        'ApprenticHD':'hipnc',
        'Education':'hipnc'
    }
    lic = hou.licenseCategory().name()
    ext = lic_dict[lic]

    #Build Filename

    filename = '{path}/{name}.{ext}'.format(path=save_path,name='-'.join(components),ext=ext)
    print (filename)

    #save
    hou.hipFile.save(filename)
