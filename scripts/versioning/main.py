import hou


def setFrameRange(kwargs):
    node = kwargs['node']
    vers = node.parm('frame_range').eval()
    
    if (vers==1):
        node.parm('f_rgx').setExpression('hou.playbar.frameRange()[0]',language =hou.exprLanguage.Python)
        node.parm('f_rgy').setExpression('hou.playbar.frameRange()[1]',language =hou.exprLanguage.Python)
        node.parm('f_rgz').setExpression('1',language =hou.exprLanguage.Python)
        # group.append(parm_range)


def getParmGroup(kwargs):
    node = kwargs['node']
    node = hou.node('obj/ground/back_forward1')
    definition = node.type().definition()
    group = definition.parmTemplateGroup()
    
    return group

    