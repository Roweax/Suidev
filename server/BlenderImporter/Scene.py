#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mathutils
import bpy
import json
import random
from Config import Config
from Planet import Planet
from Material import *
from Texture import Texture
from Model import Model
from Entity import Entity
import Color
import State
from random import choice
import time
from datetime import datetime

class Scene(object):
    """description of class"""
    def __init__(self):
        self.Obejcts = []
        self.Materials = {}
        self.render_result = []


    def AddObject(self, object):
        self.Obejcts.append(object)

    def AddMaterial(self, material):
        self.Materials[material.name] = material;

    def LoadResource(self):
        self.resource = {}
        f = open(Config.resource_path + 'resource.json')
        resource_info = json.loads(f.read())
        self.resource['hdris'] = {}
        for hdri_info in resource_info['HDRIs']:
            name = hdri_info['id']
            self.resource['hdris'][name] = hdri_info

    def OpenFile(self, file_name) :
        bpy.ops.wm.open_mainfile(filepath = Config.resource_path + file_name + ".blend")

    def LoadLibrary(self, file_name) :

        with bpy.data.libraries.load(Config.resource_path + file_name + '.blend') as (data_from, data_to):
            for attr in dir(data_to):
                #if attr == 'images' or attr == 'meshes'or attr == 'cameras' or attr == 'lamps' or attr == 'materials' or attr == 'textures' or attr == 'objects':
                setattr(data_to, attr, getattr(data_from, attr))
                print(getattr(data_from, attr))
                #    for obj in data_to.objects:
                #        if obj is not None:
                #           bpy.context.scene.objects.link(bpy.data.objects[obj])
            for attr in dir(bpy.data):
                l = getattr((bpy.data), attr)
                try :
                    for i in l:
                        print(i)
                except:
                    print('')
            for obj in data_to.objects:
                if obj is not None:
                    bpy.context.scene.objects.link(bpy.data.objects[obj])


    def Load(self, json_file):
        self.LoadResource()
        f = open(json_file)
        scene_info = json.loads(f.read())
        #print(scene_info)

        if "Render" in scene_info.keys() :
            render_info = scene_info["Render"]
            scene = bpy.context.scene;
            scene.render.image_settings.file_format = render_info["format"]
            scene.frame_end = render_info["frame"]
            scene.cycles.samples = render_info["sample"]

        if 'Library' in scene_info.keys() :
            for library in scene_info['Library']:
                self.LoadLibrary(Config.resource_path + library + '.blend')
        
        if 'Materials' in scene_info.keys() :
            for material_info in scene_info['Materials']:
                material = Material(material_info['id'], material_info['color'])
                self.AddMaterial(material)
            self.AddMaterial(TestMaterial('Test'))
            self.AddMaterial(GlassMaterial('Glass'))
            self.AddMaterial(SimpleGlassMaterial('SimpleGlass'))
            self.AddMaterial(MetalMaterial('Metal'))
            self.AddMaterial(RandomMaterial("Rand"))
        
        if 'Objects' in scene_info.keys():
            for object_info in  scene_info['Objects']:
                entity = None
                if(object_info['type'] == 'cube') :
                    entity = Entity()
                    bpy.ops.mesh.primitive_cube_add(radius = object_info['size'], view_align=False, enter_editmode=False, location=object_info['position'], layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
                #scale = object_info['size']
                    entity.baseObject = bpy.context.object
                    print ('Add a Cube')
                elif(object_info['type'] == 'model'):
                    entity = Model(object_info['id'] + '.obj')
                    state = State.instance
                    state.model = object_info['id']
                if entity != None :
                    entity.SetMaterial(self.Materials[object_info['material']])
                    self.AddObject(entity)
        
        if 'HDR' in scene_info.keys() :
            hdr = scene_info['HDR']
            if hdr != None :
                if hdr == 'rand' :
                    self.SetEnvironmentMap('{0:02d}.hdr'.format(random.randint(1, 10)))
                else :
                    self.SetEnvironmentMap(hdr + ".hdr")
        else :
            bpy.context.scene.cycles.film_transparent = True

        if 'Camera' in scene_info.keys() : 
            camera_info = scene_info['Camera']
            camera = bpy.data.objects['Camera']
            camera.location = camera_info['position']
            self.LookAt(camera, camera_info['look'])


        if 'Animation' in scene_info.keys() :
            bpy.ops.object.empty_add()
            empty_object = bpy.context.object


    def LookAt(self, obj_camera, point):
        loc_camera = obj_camera.matrix_world.to_translation()
        direction = mathutils.Vector(point) - obj_camera.location
        # point the cameras '-Z' and use its 'Y' as up
        rot_quat = direction.to_track_quat('-Z', 'Y')
        # assume we're using euler rotation
        obj_camera.rotation_euler = rot_quat.to_euler()
        #obj_camera.rotation_euler = (3.14159 / 180 * 90, 0, 0)
        bpy.data.cameras['Camera'].lens = 35;
        bpy.data.cameras['Camera'].sensor_width = 50;


    def SetEnvironmentMap(self, file_path):
        world = bpy.context.scene.world
        world.use_nodes = True
        nodes = world.node_tree.nodes

        imageNode = nodes.new('ShaderNodeTexEnvironment')
        imageNode.name = 'EnvMap'
        imageNode.image = bpy.data.images.load(Config.resource_path + file_path)

        node = nodes.new('ShaderNodeBackground')
        node.inputs[1].default_value = self.resource['hdris'][file_path]['strength']
        world.node_tree.links.new(imageNode.outputs[0], node.inputs[0])
        world.node_tree.links.new(node.outputs[0], nodes['World Output'].inputs[0])

        texcoord_node = nodes.new('ShaderNodeTexCoord')
        mapping_node = nodes.new('ShaderNodeMapping')
        mapping_node.rotation = (0, 0, 3.14159 / 180 * self.resource['hdris'][file_path]['rotation'])
        world.node_tree.links.new(texcoord_node.outputs[0], mapping_node.inputs[0])
        world.node_tree.links.new(mapping_node.outputs[0], imageNode.inputs[0])
        state = State.instance
        state.scene = self.resource['hdris'][file_path]["name"]

    def CoreRender(self, animation):
        start = datetime.now()
        bpy.ops.render.render(animation=animation, write_still = True)
        end = datetime.now()
        escape = (end - start).seconds
        return escape

    def GetRenderParams(self):
        scene = bpy.context.scene
        params = {}
        params["sample"] = scene.cycles.samples
        params["x"] = scene.render.resolution_x * scene.render.resolution_percentage / 100
        params["y"] = scene.render.resolution_y * scene.render.resolution_percentage / 100
        params["format"] = scene.render.image_settings.file_format

        if params["format"] == "H264" :
            params["fps"] = 24
        else :
            params["fps"] = 0
        return params

    def AddRenderResult(self, result) :
        self.render_result.append(result)


    def GetRenderResult(self) :
        return self.render_result


class SpaceScene(Scene):
    def __init__(self):
        super(SpaceScene, self).__init__()
        self.main_h = 0
        self.second_h = 0
        self.main_color = None
        self.second_color = None
        self.has_ring = random.random() > 0.7
        self.ring_color = None
        self.kind = ""


    def Load(self) :
        self.OpenFile("planet")
        #super(Scene, self).Load(Config.resource_path + "space.json")
        self.main_h = random.random()
        self.second_h = random.random()

        if self.has_ring :
            self.ShowRing()
        else :
            bpy.data.objects["Camera"].location[1] = 6

        kinds = ['earth', 'moon', 'hot', 'gas']
        kind = choice(kinds)
        self.kind = kind
        #kind = 'earth'
        if kind == 'earth' :
            self.ShowRandomEarth()
        elif kind == 'moon' :
            self.ShowRandomMoon()
        elif kind == 'hot':
            self.ShowRandomHot()
        elif kind == 'gas' :
            self.ShowRandomGas()

    
    def ShowObjects(self, name_list) :
        for mesh_name in name_list :
            self.ShowObject(mesh_name)


    def ShowObject(self, name) :
        bpy.data.objects[name].hide = False;
        bpy.data.objects[name].hide_render = False;

    def GetMaterialNodes(self, name) :
        bpy_object = bpy.data.objects[name];
        return bpy_object.material_slots[0].material.node_tree.nodes;

    def RandomNoise(self) :
        #noise
        node = bpy.data.node_groups["Oil.003"].nodes["Mapping"]
        node.translation[0] = random.random() * 50
        node.translation[1] = random.random() * 50
        node.translation[2] = random.random() * 50
        scale = random.random() + 0.5
        node.scale[0] = scale
        node.scale[1] = scale
        node.scale[2] = scale

    def ShowRandomEarth(self) :
        self.ShowObjects(['Planet_Procedural', 'Planet_ATMOS', 'Planet_Clouds', 'Planet_Clouds.Outer', 'Planet_LightsMask'])
        nodes = self.GetMaterialNodes('Planet_Procedural')

        #land
        color2 = Color.HSL_to_RGB(self.main_h, 0.7, 0.7)
        nodes["Mix.016"].inputs[2].default_value = Color.RGB_to_RGBA(color2)
        #ocean
        color = Color.HSL_to_RGB(self.second_h, 1.0, 0.5)
        nodes["Mix.017"].inputs[2].default_value = Color.RGB_to_RGBA(color)

        nodes = self.GetMaterialNodes('Planet_ATMOS')
        color3 = Color.HSL_to_RGB(self.second_h + (random.random() - 0.5) * 0.01, 0.6, 0.25)
        nodes["Emission"].inputs[0].default_value =Color.RGB_to_RGBA(color3)

        has_cloud = random.random() > 0.3
        if has_cloud :
            nodes = self.GetMaterialNodes('Planet_Clouds')
            color4 = Color.HSL_to_RGB(self.main_h + (random.random() - 0.5) * 0.05, 0.3, random.random() * 0.7)
            nodes["ColorRamp.002"].color_ramp.elements[1].color = Color.RGB_to_RGBA(color4)
        
        self.RandomNoise();


    def ShowRandomMoon(self) :
        self.ShowObjects(['Planet_Moon'])
        nodes = self.GetMaterialNodes('Planet_Moon')

        color = Color.HSL_to_RGB(self.main_h, 0.05, 0.7)
        nodes["Mix.016"].inputs[2].default_value = (color[0], color[1], color[2], 1.0)

        color2 = Color.HSL_to_RGB(self.main_h + (random.random() - 0.5) * 0.1, 1.0, 0.9)
        nodes["Mix.017"].inputs[2].default_value = Color.RGB_to_RGBA(color2)

        nodes = self.GetMaterialNodes('Planet_Rings')
        color = Color.HSL_to_RGB(self.main_h, 1.0, 0.92)
        nodes["Diffuse BSDF"].inputs[0].default_value = (color[0], color[1], color[2], 1.0)
        
        self.RandomNoise();

    def ShowRandomHot(self) :
        self.ShowObjects(['Planet_Procedural.Hot', 'Planet_ATMOS.Hot', 'Planet_Clouds.Hot', 'Planet_Clouds.Outer.Hot', 'Planet_LightsMask.Hot'])
        nodes = self.GetMaterialNodes('Planet_Procedural.Hot')

        color = Color.HSL_to_RGB(self.main_h, 1, 0.5)
        nodes["Mix.017"].inputs[2].default_value = (color[0], color[1], color[2], 1.0)
        color2 = Color.HSL_to_RGB(self.main_h + (random.random() -0.5)* 0.1, 1.0, 0.58)
        nodes["Mix.016"].inputs[2].default_value = (color2[0], color2[1], color2[2], 1.0)

        nodes = self.GetMaterialNodes('Planet_ATMOS.Hot')
        color3 = Color.HSL_to_RGB(self.main_h + (random.random() - 0.5) * 0.05, 0.6, 0.25)
        nodes["Emission"].inputs[0].default_value = (color3[0], color3[1], color3[2], 1.0)
        
        self.RandomNoise();

    def ShowRandomGas(self) :
        self.ShowObjects(['Planet_Gas'])
        nodes = self.GetMaterialNodes('Planet_Gas')

        color = Color.HSL_to_RGB(self.main_h, 0.6, 0.2) 
        nodes["Mapping"].scale[2] = random.random() + 0.8
        nodes["Mapping"].translation[0] = random.random() * 10
        nodes["Mapping"].translation[1] = random.random() * 10
        nodes["Mapping"].translation[2] = random.random() * 10
        nodes["Mix.001"].inputs[2].default_value = (color[0], color[1], color[2], 1.0)

    def ShowRing(self) :
        self.ShowObject('Planet_Rings')

        nodes = self.GetMaterialNodes('Planet_Rings')
        color = Color.HSL_to_RGB(self.main_h, 1.0, 0.92)
        nodes["Diffuse BSDF"].inputs[0].default_value = (color[0], color[1], color[2], 1.0)

        nodes["Noise Texture"].inputs[1].default_value = 1.0 + random.random() * 3
        nodes["Noise Texture"].inputs[2].default_value = 1.0 + random.random() * 3
        nodes["Noise Texture"].inputs[3].default_value = 1.0 + random.random() * 3



    def Render(self) :
        '''Render Video'''
 
        bpy.context.scene.frame_start = 0
        bpy.context.scene.frame_end = 239
        bpy.context.scene.frame_step = 1
        bpy.context.scene.cycles.samples = 30
        bpy.context.scene.cycles.film_transparent = False
        bpy.context.scene.render.image_settings.file_format = 'H264'
        bpy.context.scene.render.ffmpeg.format = 'MPEG4'
        bpy.context.scene.render.ffmpeg.codec = 'H264'
        bpy.context.scene.render.resolution_percentage = 40
        bpy.context.scene.render.filepath = Config.data_path+ "temp/"
        result = self.GetRenderParams()
        result["frame"] = 0
        result["length"] = 10
        result["rotate"] = (15, 15, 0)
        result["light_angle"] = 0
        result["render_time"] = self.CoreRender(True)
        self.render_result.append(result)
        

        '''Render Images'''
        step = 20
        for i in range(0, 239, step):
            bpy.context.scene.frame_start = i
            bpy.context.scene.frame_end = i
            bpy.context.scene.frame_step = step
            bpy.context.scene.cycles.samples = 90
            bpy.context.scene.cycles.film_transparent = False 
            bpy.context.scene.render.image_settings.file_format = 'PNG'
            bpy.context.scene.render.image_settings.color_mode = 'RGB'
            bpy.context.scene.render.resolution_percentage = 100
            bpy.context.scene.render.filepath = Config.data_path+ "temp/"
            result = self.GetRenderParams()
            result["frame"] = i
            result["length"] = 0
            result["rotate"] = (15, 15, 1.0 * i / 240 * 360)
            result["light_angle"] = -1.0 * i / 240 * 360
            result["render_time"] = self.CoreRender(True)
            self.AddRenderResult(result)

        State.instance.Set("result", self.GetRenderResult())

        planet = {}
        planet["kind"] = self.kind
        planet["ring"] = self.has_ring
        State.instance.Set("planet", planet)
