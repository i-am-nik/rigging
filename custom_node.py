import maya.OpenMaya as om
import maya.OpenMayaMPx as ompx

# Node name and ID
kPluginNodeName = "AddTwoFloatsNode"
kPluginNodeId = om.MTypeId(0x8700A)  # Unique ID, make sure to generate your own

class AddTwoFloatsNode(ompx.MPxNode):
    # Attribute handles
    input1 = None
    input2 = None
    output = None

    def __init__(self):
        ompx.MPxNode.__init__(self)

    def compute(self, plug, dataBlock):
        if plug == AddTwoFloatsNode.output:
            # Get input values
            input1Value = dataBlock.inputValue(AddTwoFloatsNode.input1).asFloat()
            input2Value = dataBlock.inputValue(AddTwoFloatsNode.input2).asFloat()

            # Compute the output value
            outputValue = input1Value + input2Value

            # Set the output value
            outputHandle = dataBlock.outputValue(AddTwoFloatsNode.output)
            outputHandle.setFloat(outputValue)
            dataBlock.setClean(plug)
        else:
            return om.kUnknownParameter

def nodeCreator():
    return AddTwoFloatsNode()

def nodeInitializer():
    # Create attributes
    nAttr = om.MFnNumericAttribute()

    AddTwoFloatsNode.input1 = nAttr.create("input1", "in1", om.MFnNumericData.kFloat, 0.0)
    nAttr.readable = True
    nAttr.writable = True
    nAttr.storable = True

    AddTwoFloatsNode.input2 = nAttr.create("input2", "in2", om.MFnNumericData.kFloat, 0.0)
    nAttr.readable = True
    nAttr.writable = True
    nAttr.storable = True

    AddTwoFloatsNode.output = nAttr.create("output", "out", om.MFnNumericData.kFloat, 0.0)
    nAttr.readable = True
    nAttr.writable = False
    nAttr.storable = False

    # Add attributes to the node
    AddTwoFloatsNode.addAttribute(AddTwoFloatsNode.input1)
    AddTwoFloatsNode.addAttribute(AddTwoFloatsNode.input2)
    AddTwoFloatsNode.addAttribute(AddTwoFloatsNode.output)

    # Set attribute dependencies
    AddTwoFloatsNode.attributeAffects(AddTwoFloatsNode.input1, AddTwoFloatsNode.output)
    AddTwoFloatsNode.attributeAffects(AddTwoFloatsNode.input2, AddTwoFloatsNode.output)

def initializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.registerNode(kPluginNodeName, kPluginNodeId, nodeCreator, nodeInitializer, ompx.MPxNode.kDependNode)
    except:
        om.MGlobal.displayError("Failed to register node: " + kPluginNodeName)

def uninitializePlugin(mobject):
    mplugin = ompx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kPluginNodeId)
    except:
        om.MGlobal.displayError("Failed to deregister node: " + kPluginNodeName)