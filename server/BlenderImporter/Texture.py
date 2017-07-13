import bpy

class Texture(object):
    def __init__(self, name, file_path):
        self.name = name
        self.baseTexture = bpy.dat.textures.new('EVN_MAP', 'ENVIRONMENT_MAP')
        self.baseTexture.image = bpy.data.images.load(file_path)
