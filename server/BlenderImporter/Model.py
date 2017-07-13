import bpy
from Entity import Entity
from Config import Config

class Model(Entity):
    def __init__(self, name):
        bpy.ops.import_scene.obj(filepath=Config.resource_path + name, axis_forward='-Z', axis_up='Y', filter_glob="*.obj")
        self.baseObject = bpy.context.scene.objects['Model']
        self.baseObject.rotation_euler = (3.14159 / 180 * 90, 0, 3.14159 / 180 * 30)
        #print('Load ' + name + '.obj')
        
