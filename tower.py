import bpy

def create_cube(name, size, location):
    bpy.ops.mesh.primitive_cube_add(size=size, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_cylinder(name, radius, depth, location):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_cone(name, radius, depth, location):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=radius, radius2=0, depth=depth, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

# Delete all existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create the tower base (cylinder)
tower_base = create_cylinder("Tower_Base", 2, 0.5, (0, 0, 0.25))

# Create tower body (cylinder)
tower_body = create_cylinder("Tower_Body", 1, 10, (0, 0, 5.25))

# Create tower top (cone)
tower_top = create_cone("Tower_Top", 1.5, 2, (0, 0, 10.75))

# Create battlements (cubes)
battlement_count = 8
radius = 1.5
