import bpy
import bmesh
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Class for Cube
class Cube:
    def __init__(self, location=(0, 0, 0), size=2):
        self.location = location
        self.size = size
        self.create_cube()

    def create_cube(self):
        bpy.ops.mesh.primitive_cube_add(size=self.size, enter_editmode=False, align='WORLD', location=self.location)
        self.cube_object = bpy.context.active_object
        
# Class for Parallelepiped
class Parallelepiped:
    def __init__(self, location=(0, 0, 0), size=(2, 2, 2)):
        self.location = location
        self.size = size
        self.create_parallelepiped()
        
    def create_parallelepiped(self):
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=self.location)
        bpy.ops.transform.resize(value=self.size)
        self.parallelepiped_object = bpy.context.active_object
        self.parallelepiped_object.name = 'Parallelepiped'  # set the name of the object

# Class for Sphere
class Sphere:
    def __init__(self, location=(0, 0, 0), radius=1):
        self.location = location
        self.radius = radius
        self.create_sphere()

    def create_sphere(self):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=self.radius, enter_editmode=False, align='WORLD', location=self.location)
        self.sphere_object = bpy.context.active_object
        self.sphere_object.name = 'Sphere'  # set the name of the object

# Class for Cone
class Cone:
    def __init__(self, location=(0, 0, 0), radius=1, height=2):
        self.location = location
        self.radius = radius
        self.height = height
        self.create_cone()

    def create_cone(self):
        bpy.ops.mesh.primitive_cone_add(radius1=self.radius, depth=self.height, enter_editmode=False, align='WORLD', location=self.location)
        self.cone_object = bpy.context.active_object
        self.cone_object.name = 'Cone'  # set the name of the object
        
class Pyramid:
    def __init__(self, location=(0, 0, 0), base_size=2, height=2):
        self.location = location
        self.base_size = base_size
        self.height = height
        self.create_pyramid()

    def create_pyramid(self):
        bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=self.base_size / 2, depth=self.height, enter_editmode=False, align='WORLD', location=self.location)
        self.pyramid_object = bpy.context.active_object
        self.pyramid_object.name = 'Pyramid'  # set the name of the object  
              
# Create a new cube using the Cube class
cube = Cube(location=(0, 0, 0), size=4)
parallelepiped = Parallelepiped(location=(5, 0, 0), size=(4, 8, 2))
sphere = Sphere(location=(-5, 0, 0), radius=2)
cone = Cone(location=(10, 0, 0), radius=2, height=4)
cube_rotation = cube.cube_object.rotation_euler
pyramid = Pyramid(location=(-10, 0, 0), base_size=5, height = 5)
