import bpy
import random
import Color
from Config import Config
import State
class Material(object):
    def __init__(self, name, color = None):
        self.name = name
        self.color = color
        m = bpy.data.materials.new(name)

        if color == None :
            m.use_nodes = True
            nodes = m.node_tree.nodes
            node = nodes[nodes.find('BSDF_DIFFUSE')]
            nodes.remove(node)  # remove not used
        else :
            m.diffuse_color = color

        self.baseMaterial = m

    def newNode(self, kind, name = None):
        node = self.baseMaterial.node_tree.nodes.new(kind)
        if name != None :
            node.name = name
        return node

    def newLink(self, outNode, outIndex, inNode, inIndex) :
        self.baseMaterial.node_tree.links.new(outNode.outputs[outIndex], inNode.inputs[inIndex]) 

    def getNode(self, name) :
        return self.baseMaterial.node_tree.nodes[name]

    def getNodeByType(self , name) :
        nodes = self.baseMaterial.node_tree.nodes;
        return nodes[nodes.find(name)]

    def getOutputNode(self) :
        return self.baseMaterial.node_tree.nodes['Material Output']


    def createDiffuseNode(self, color) :
        node = self.newNode('ShaderNodeBsdfDiffuse')
        node.inputs[0].default_value = color
        return node

    def createMatelNode(self, color, roughness = 0.0, anisotropy = 0.0):
        node = self.newNode('ShaderNodeBsdfAnisotropic', None)# nodes.new('ShaderNodeBsdfAnisotropic')
        #node.name = 'Me'
        node.inputs[0].default_value = color
        node.inputs[1].default_value = roughness
        node.inputs[2].default_value = anisotropy
        return node

    def createGlassNode(self, color, roughness, ior) :
        node = self.newNode('ShaderNodeBsdfGlass') # nodes.new('ShaderNodeBsdfGlass')
        node.inputs[0].default_value = color
        node.inputs[1].default_value = roughness
        node.inputs[2].default_value = ior
        return node

    def createEmissionNode(self, color, strength) :
        node = self.newNode('ShaderNodeEmission')
        node.inputs[0].default_value = color
        node.inputs[1].default_value = strength
        return node

    def createSubsurfaceNode(self, color, scale):
        node = self.newNode('ShaderNodeSubsurfaceScattering')
        node.inputs[0].default_value = color
        node.inputs[1].default_value = scale
        return node

class TestMaterial(Material):
    def __init__(self, name):
        super(TestMaterial, self).__init__(name, None)
        #mat = bpy.data.materials.new(name)
        #mat.use_nodes = True
        #mat.diffuse_color = (1, 0, 0)
        # nodes = mat.node_tree.nodesi
        # support for multilanguage
        #node = nodes[nodes.find('BSDF_DIFFUSE')]
        #mat.node_tree.nodes.remove(node)  # remove not used
        nodes = self.baseMaterial.node_tree.nodes
        node = nodes.new('ShaderNodeEmission')
        node.name = 'Transparent_0'
        node.location = 250, 160
        node.inputs[0].default_value = [0.297, 0.375, 0.8, 1]
        node.inputs[1].default_value = 100
        output = self.getOutputNode()
        output.location = 700, 160

        # Connect nodes
        outn = nodes['Transparent_0'].outputs[0]
        inn = nodes['Material Output'].inputs[0]
        self.baseMaterial.node_tree.links.new(outn, inn)
        #mat.use_shadeless = True


class MetalMaterial(Material):
    def __init__(self, name):
        super(MetalMaterial, self).__init__(name, (1, 0, 0))
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node = nodes[nodes.find('BSDF_DIFFUSE')]
        mat.node_tree.nodes.remove(node)  # remove not used
        
        node = nodes.new('ShaderNodeBsdfAnisotropic')
        node.name = 'Metal'
        node.inputs[0].default_value = (0.64, 0.312, 0.044, 1.0)
        node.inputs[1].default_value = 0
        mat.node_tree.links.new(node.outputs[0], nodes['Material Output'].inputs[0])
        self.baseMaterial = mat

class SimpleGlassMaterial(Material):
    def __init__(self, name):
        super(SimpleGlassMaterial, self).__init__(name, (1, 0, 0))
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        node = nodes[nodes.find('BSDF_DIFFUSE')]
        mat.node_tree.nodes.remove(node)  # remove not used
        
        node = nodes.new('ShaderNodeBsdfAnisotropic')
        node.name = 'Glass'
        mat.node_tree.links.new(node.outputs[0], nodes['Material Output'].inputs[0])
        self.baseMaterial = mat


class GlassMaterial(Material):
    def __init__(self, name):
        super(GlassMaterial, self).__init__(name, (1, 0, 0))
        rv=0.352716
        gv=0.760852
        bv=0.9
        # Avoid duplicate materials
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        mat.diffuse_color = (rv, gv, bv)
        nodes = mat.node_tree.nodes

        # support for multilanguage
        node = nodes[nodes.find('BSDF_DIFFUSE')]
        mat.node_tree.nodes.remove(node)  # remove not used

        node = nodes.new('ShaderNodeLightPath')
        node.name = 'Light_0'
        node.location = 10, 160

        node = nodes.new('ShaderNodeBsdfGlass')
        node.name = 'Glass_0'
        node.location = 250, 300

        node = nodes.new('ShaderNodeBsdfTransparent')
        node.name = 'Transparent_0'
        node.location = 250, 0

        node = nodes.new('ShaderNodeMixShader')
        node.name = 'Mix_0'
        node.inputs[0].default_value = 0.1
        node.location = 500, 160

        node = nodes.new('ShaderNodeMixShader')
        node.name = 'Mix_1'
        node.inputs[0].default_value = 0.1
        node.location = 690, 290

        node = nodes['Material Output']
        node.location = 920, 290
        # Connect nodes
        outn = nodes['Light_0'].outputs[1]
        inn = nodes['Mix_0'].inputs[0]
        mat.node_tree.links.new(outn, inn)

        outn = nodes['Light_0'].outputs[2]
        inn = nodes['Mix_1'].inputs[0]
        mat.node_tree.links.new(outn, inn)

        outn = nodes['Glass_0'].outputs[0]
        inn = nodes['Mix_0'].inputs[1]
        mat.node_tree.links.new(outn, inn)
   
        outn = nodes['Transparent_0'].outputs[0]
        inn = nodes['Mix_0'].inputs[2]
        mat.node_tree.links.new(outn, inn)

        outn = nodes['Mix_0'].outputs[0]
        inn = nodes['Mix_1'].inputs[1]
        mat.node_tree.links.new(outn, inn)

        outn = nodes['Mix_1'].outputs[0]
        inn = nodes['Material Output'].inputs[0]
        mat.node_tree.links.new(outn, inn)
        self.baseMaterial = mat


class RandomMaterial(Material) :
    def __init__(self, name):
        super(RandomMaterial, self).__init__(name)
        
        color = (random.random(), random.random(), random.random(), 1.0)
        rgb = Color.HSL_to_RGB(random.random(), 0.6, 0.6)
        
        rgb2 = Color.HSL_to_RGB(random.random(), 0.9, 0.5)
        color =(rgb[0], rgb[1], rgb[2], 1.0)
        color2 = (rgb2[0], rgb2[1], rgb2[2], 1.0)
        print( color)
        kind = random.randint(0, 9)
        state = State.instance
        if kind <=3 :
            node = None
            if kind == 0 :
                node = self.createMatelNode(color)
                state.material_name = "metal"
            elif kind == 1:
                pure = random.randint(0, 1)
                if pure == 0:
                    node = self.createGlassNode(color, 0, 1.45)
                else :
                    node = self.createGlassNode(color, random.uniform(0.1, 0.5), 1.45)
                state.material_name = "glass"
            elif kind == 2:
                node = self.createDiffuseNode(color)
                state.material_name = "diffuse"
            elif kind == 3:
                node = self.createSubsurfaceNode(color, 1)
                state.material_name = "subsurface"
            state.color = color 
            self.baseMaterial.node_tree.links.new(node.outputs[0], self.getOutputNode().inputs[0])
        else :
            mat = None
            if kind == 4 :
                mat = CarPaintMaterial(color2)
                state.material_name = "car paint"
            elif kind == 5 :
                mat = GalvanizedMetalMaterial(random.uniform(0.0, 1.0))
                state.material_name = "galvanized metal"
            elif kind == 6 :
                mat = PianoPaintMaterial(color2)
                state.material_name = "paino paint"
            elif kind == 7 :
                mat = LollipopMaterial(color2)
                state.material_name = "lollipop"
            elif kind == 8:
                mat = LegoPlasticMaterial(color2)
                state.material_name = "lego plastic"
            elif kind == 9:
                mat = LedMaterial(color2)
                state.material_name = "led"
            self.baseMaterial = mat.baseMaterial
            state.color = color2

class LibraryMaterial(Material) :
    def __init__(self, file_path, material_name):
        super(LibraryMaterial, self).__init__("")
#    def loadLibraryNode(self, file_name, material_name) :
        with bpy.data.libraries.load(Config.resource_path + "Material/" + file_path + '.blend') as (data_from, data_to):
            data_to.materials = data_from.materials
        self.baseMaterial = bpy.data.materials[material_name]



class CarPaintMaterial(LibraryMaterial):
    def __init__(self, color):
        super(CarPaintMaterial, self).__init__("20-car-paint", "BMD_CarPaint_0020")
        node = self.getNodeByType("BMD_CarPaintShader")
        node.inputs[0].default_value = color;
        node.inputs[2].default_value = color;

        rgb = (color[0], color[1], color[2])
        hsl = Color.RGB_to_HSL(color[0], color[1], color[2])
        rgb = Color.HSL_to_RGB(hsl[0], hsl[1], hsl[2]/2)

        node.inputs[1].default_value = (color[0], color[1], color[2], 1.0)

class GalvanizedMetalMaterial(LibraryMaterial):
    def __init__(self, roughness):
        super(GalvanizedMetalMaterial, self).__init__("21-galvanized-metal", "BMD_GalvanizedMetal_0021")
        node = self.getNodeByType("ShaderNodeBsdfAnisotropic")
        node.inputs[1].default_value = roughness


class PianoPaintMaterial(LibraryMaterial):
    def __init__(self, color):
        super(PianoPaintMaterial, self).__init__("38-piano-paint", "palette")
        node = self.getNode("RGB")
        node.outputs[0].default_value = color


class LollipopMaterial(LibraryMaterial) :
    def __init__(self, color):
        super(LollipopMaterial, self).__init__("63-lollipop", "BMD_Lollipop")
        node = self.getNodeByType("BMD_LollipopShader")
        node.inputs[0].default_value = color;

class LegoPlasticMaterial(LibraryMaterial) :
    def __init__(self, color):
        super(LegoPlasticMaterial, self).__init__("62-lego-abs-plastic", "BMD_LegoPlastic")
        node = self.getNodeByType("BMD_LegoPlasticShader")
        node.inputs[0].default_value = color


class LedMaterial(LibraryMaterial):
    def __init__(self, color):
        super(LedMaterial, self).__init__("64-green-led_emission", "green1-LED")
        node = self.getNode("Emission")
        node.inputs[0].default_value = color
