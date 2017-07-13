import bpy
from Entity import Entity
from Material import Material

class Planet(Entity):
    """description of class"""
    def __init__(self, token, kind, ring, radius, position, emission):
        super(Entity,self).__init__()
        self.token = token
        self.radius = radius
        self.position = position
        self.emission = emission
        self.kind = kind

        if kind == 'earth' :
            k = ''
        elif kind == 'moon' :
            k = ''
        elif kind == 'sun' :
            k = ''
        
    #def Render(self):
        #bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, size=self.radius, view_align=False, enter_editmode=False, location=self.position, rotation=(0.0, 0.0, 0.0), layers=(True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))
        #bpy.context.object.data.materials.append(self.material.baseMaterial)
        #self.SetBaseObject(bpy.context.object)
        
        #material = PlanetMaterial('', 'mas.png', emission)
        #self.SetMaterial(material)


class Sun(Planet):
    def __init__(self, token, radius, position):
        super(Planet, self).__init__(token, radius, position)

        #add lamp

    #def Render(self):
    #    super(Material, self).Render()


class PlanetMaterial(Material):
    def __init__(self, name, imageName, emission):
        super(TestMaterial, self).__init__(name, None)
        
        image_node = self.newNode('ShaderNodeTexImage', '')
        image_node.image = bpy.data.images.load('./Resource/Texture/' + imageName)

        rgbcurve = self.newNode('RGBCurve', '')
        self.newLink(imageNode, 1, rgbcurve, 0)
        #curev prams.................
    
        fresenl_node = self.newNode('Frensel', '')
        fresenl_node.inputs[0].default_value = 1.45 #IOR

        


        # Connect nodes
        outn = nodes['Transparent_0'].outputs[0]
        inn = nodes['Material Output'].inputs[0]
        mat.node_tree.links.new(outn, inn)
        #mat.use_shadeless = True
        


 
