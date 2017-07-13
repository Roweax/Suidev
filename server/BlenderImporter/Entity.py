import bpy

class Entity(object):
    def __init__(self):
        self.material = None
        self.baseObject = None
        self.children = []

    def AddChild(self, child):
        self.children.append(child)
   
    def SetBaseObject(self, bo):
        self.baseObject = bo

    def SetMaterial(self, material):
        self.material = material
        #print (self.baseObject)
        if len(self.baseObject.material_slots) < 1:
        # if there is no slot then we append to create the slot and assign
            self.baseObject.data.materials.append(material.baseMaterial)
        else:
            # we always want the material in slot[0]
            self.baseObject.material_slots[0].material = material.baseMaterial

