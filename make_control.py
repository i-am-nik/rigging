import maya.cmds as cmds
import maya.mel as mel

#make_controls(['test_joint'],translateX=1)
def make_controls(objects,**kwargs):
    ''' 
    This methods generates controls for your rig based on given inputs.
    Input keys and their accepted values can be found below:
    
    parent : [str] (group where you want to keep all your controls)
    global : [str] (global control name of your rig; module connections will be added here)
    module : [str] (parent group for controls; control connections will be added here)
    level  : [str] (primary, secondary, tertiary) (level of controls)
    pivot  : [int] (use this flag to create separate pivot control for main control)
    alphaNaming : [int] (use this flag to give sequential alphabatical naming to all controls, keep this flag off to use default numeric sequential naming)
    color : [str] (yellow, red, blue, light yellow, light red, light blue, green) (pass on a color name to this flag to make your control of that color)
    shape :  [str] (circle, square, triangle, rectangle, sphere, cone, cube, star) (pass on a shape to make control)
    worldOrient : [int] (turn this flag to make world oriented control)
    mirror : [int] (turn this flag to mirror the control; if you provide a left side joint it will look for its right side mirror and vice versa)
    translate : [int] (turn this flag to enable translate channels of control)
    rotate : [int] (turn this flag to enable rotate channels of control)
    scale : [int] (turn this flag to enable scale channels of control)
    translateX, translateY, translateZ : [int] (use these flags to enable or disable individual translate channels) 
    rotateX, rotateY, rotateZ : [int] (use these flags to enable or disable individual rotation channels) 
    scaleX, scaleY, scaleZ : [int] (use these flags to enable or disable individual scale channels)
    spaces : [list] (pass on the object you want control to have space switch to)
    spaceNames : [list] (pass on the names you want those objects to identify by)

    '''

    # controls parent
    parent = kwargs.get('parent',"")

    # global control
    global_control = kwargs.get('global',"")

    # primary name of all the groups and controls
    module_name = kwargs.get('module',"control_module")
    
    # type of control : primary, secondary, tertiary
    level = kwargs.get('level','primary')
    
    # separate pivot control for the control
    control_pivot = kwargs.get('pivot',0)
    
    # alpha sequential naming for all the passed objects
    alpha_sequence_naming = kwargs.get('alphaNaming',0)

    # color of the control : yellow, red, blue, light yellow, light red, light blue, green
    color = kwargs.get('color',"yellow")
    # shape of the control : circle, square, triangle, rectangle, sphere, cone, cube, star
    shape = kwargs.get('shape',"circle")

    #world orient of the control switch
    world_orient = kwargs.get('worldOrient',0)

    # find mirror side of the control ; 'l_","left_","_left"
    mirror = kwargs.get('mirror',0)

    # translate channels switch
    translate = kwargs.get('translate',0)
    # rotate channels switch
    rotate = kwargs.get('rotate',0)
    # scale channels switch
    scale = kwargs.get('scale',0)

    # translate channel switch for indivual axis
    translateX = kwargs.get('translateX',0)
    translateY = kwargs.get('translateY',0)
    translateZ = kwargs.get('translateZ',0)

    # rotate channel switch for indivual axis
    rotateX = kwargs.get('rotateX',0)
    rotateY = kwargs.get('rotateY',0)
    rotateZ = kwargs.get('rotateZ',0)

    # scale channel switch for indivual axis
    scaleX = kwargs.get('scaleX',0)
    scaleY = kwargs.get('scaleY',0)
    scaleZ = kwargs.get('scaleZ',0)

    spaces = kwargs.get('spaces',"")
    space_names= kwargs.get('spaceNames',"")

    # setting indiviual axis on if transform is on
    if translate:
        translateX = 1
        translateY = 1
        translateZ = 1

    if rotate:
        rotateX = 1
        rotateY = 1
        rotateZ = 1

    if scale:
        scaleX = 1
        scaleY = 1
        scaleZ = 1

    # array to store all the controls
    control_groups = []
    
    for object in objects:
        control = get_shape(shape)
        control_name = cmds.rename(control[0],(object+'_control'))
        match_control(control_name,object)
        control_offset_group = create_offset_group(control_name)
        control_groups.append(control_offset_group)

        if translateX == 0:
            cmds.setAttr((control_name+'.tx'),lock=True,keyable=False,channelBox=False)

        if translateY == 0:
            cmds.setAttr((control_name+'.ty'),lock=True,keyable=False,channelBox=False)

        if translateZ == 0:
            cmds.setAttr((control_name+'.tz'),lock=True,keyable=False,channelBox=False)

        if rotateX == 0:
            cmds.setAttr((control_name+'.rx'),lock=True,keyable=False,channelBox=False)

        if rotateY == 0:
            cmds.setAttr((control_name+'.ry'),lock=True,keyable=False,channelBox=False)

        if rotateZ == 0:
            cmds.setAttr((control_name+'.rz'),lock=True,keyable=False,channelBox=False)

        if scaleX == 0:
            cmds.setAttr((control_name+'.sx'),lock=True,keyable=False,channelBox=False)

        if scaleY == 0:
            cmds.setAttr((control_name+'.sy'),lock=True,keyable=False,channelBox=False)

        if scaleZ == 0:
            cmds.setAttr((control_name+'.sz'),lock=True,keyable=False,channelBox=False)

    return control_groups


def get_shape(shape):
    # TODO: return circle shape for now, will add other shapes later
    if shape == 'circle':
        control_transform = cmds.circle(n='test_circle_control')
    
    cmds.delete(control_transform[0],ch=True)
    return control_transform

def match_control(control,transform):
    pc = cmds.pointConstraint(transform,control)
    oc = cmds.orientConstraint(transform,control)
    cmds.delete(pc,oc)

def create_offset_group(transform): 
    ''' This method creates and returns offset group of the given input'''

    # create one empty group at world named as per given transform
    offset_group = cmds.group(em=True,w=True,n=(transform+'_offset_group'))
    
    # set rotate order of new group same as transform
    rotate_order = cmds.getAttr(transform+'.rotateOrder')
    cmds.setAttr(offset_group+'.rotateOrder',rotate_order)

    # match transforms of new group with transform using point, orient and scale constraints
    pc = cmds.pointConstraint(transform,offset_group)
    oc = cmds.orientConstraint(transform,offset_group)
    sc = cmds.scaleConstraint(transform,offset_group)
    
    # delete these constraints
    cmds.delete(pc,oc,sc)

    # parent transform under offset group
    cmds.parent(transform,offset_group)

    # check if given input is joint
    if cmds.nodeType(transform)=='joint':
        for channel in {'.rotate','.jointOrient'}:
            for axis in ('X','Y','Z'):
                # remove values of rotate and jointOrient
                cmds.setAttr(transform+channel+axis,0)

    return offset_group