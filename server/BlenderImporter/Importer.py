import bpy
import os
import shelve
from mathutils import *
from math import *
from Config import Config
import State
from Scene import *
import dbm
class Importer(object):
    """description of class"""
    def __init__(self):
        aa = 1
        #delete the cube
        bpy.ops.object.delete(use_global=True)
        
        # Add a camera fish eye.
        #bpy.ops.object.camera_add(view_align=True, location=(0, 0, 2.5), rotation=(0, 0, 0))
        #bpy.context.object.rotation_euler[0] = 0
        #bpy.context.object.rotation_euler[1] = 0
        #bpy.context.object.rotation_euler[2] = 0
        #bpy.context.object.data.type = 'PANO'
        #bpy.context.object.data.cycles.fisheye_lens = 2.7
        #bpy.context.object.data.cycles.fisheye_fov = 3.14159
        #bpy.context.object.data.sensor_width = 8.8
        #bpy.context.object.data.sensor_height = 6.6
        
    def Render(self, xmlfile):
        (name, fileext) = os.path.splitext(xmlfile)
        scene = SpaceScene()
        #Add a lamp.
        #bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location=(0, 1.5, 2.5), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #bpy.context.object.data.shadow_soft_size = 0.01
        #bpy.context.object.data.cycles.cast_shadow = True
        #Render results
        #Set the rendering parameter
        
        state = State.instance
        state.width = 980
        state.height = 540
        state.sample = 100
        state.file_format = "PNG"
        bpy.context.scene.render.engine = 'CYCLES'
        bpy.context.scene.render.pixel_aspect_x = 1
        bpy.context.scene.render.pixel_aspect_y = 1
        bpy.context.scene.render.use_file_extension = True
        bpy.context.scene.render.image_settings.color_mode ='RGBA'
        bpy.context.scene.render.image_settings.file_format = state.file_format
        #bpy.context.scene.render.filepath = Config.data_path + name[name.rfind('/') + 1:] + "/" 
        bpy.context.scene.render.filepath = Config.data_path+ "temp/"
        bpy.context.scene.render.image_settings.compression = 90
        ##sampling;=path tracing 
        bpy.context.scene.cycles.progressive = 'PATH'
        bpy.context.scene.cycles.samples = state.sample
        bpy.context.scene.cycles.max_bounces = 1
        bpy.context.scene.cycles.min_bounces = 1
        bpy.context.scene.cycles.glossy_bounces = 1
        bpy.context.scene.cycles.transmission_bounces = 1
        bpy.context.scene.cycles.volume_bounces = 1
        bpy.context.scene.cycles.transparent_max_bounces = 1
        bpy.context.scene.cycles.transparent_min_bounces = 1
        bpy.context.scene.cycles.use_progressive_refine = True
        bpy.context.scene.render.tile_x = 64
        bpy.context.scene.render.tile_y = 64
        
        scene.Load()
        #bpy.context.scene.render.resolution_x = state.width * 2
        #bpy.context.scene.render.resolution_y = state.height * 2
        #bpy.context.scene.render.resolution_percentage = 50
        bpy.context.scene.frame_start = 1
        bpy.context.scene.frame_end = 1
        bpy.context.scene.frame_step = 1
        bpy.context.scene.render.image_settings.file_format = state.file_format
        bpy.context.scene.cycles.samples = state.sample
        bpy.context.scene.cycles.progressive = 'PATH'
        bpy.context.scene.cycles.use_progressive_refine = True
        scene.Render()
        #bpy.ops.render.render(animation=True)
        #render_data_file = shelve.Shelf(dbm.open(Config.data_path + "temp/render", 'w'))
        render_data_file = shelve.open(Config.data_path + "temp/render", protocol=2, writeback=True)
        render_data_file["render"] = state
        render_data_file.close()


