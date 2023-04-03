import bpy
import math
import random

def create_material(name, color, use_nodes=False):
    material = bpy.data.materials.new(name)
    material.use_nodes = use_nodes
    if not use_nodes:
        material.diffuse_color = color + (1,)
    return material

def create_pyramid(name, size, location):
    bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=size, radius2=0, depth=size, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_cube(name, size, location):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0], size[1], size[2])
    return obj

def create_cylinder(name, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=radius, depth=depth, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rotation
    return obj

def create_cone(name, radius, depth, location):
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=radius, radius2=0, depth=depth, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj

def create_torus(name, location):
    bpy.ops.mesh.primitive_torus_add(align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name

def create_tower(name_prefix, base_radius, base_height, body_radius, body_height, top_radius, top_height, location):
    tower_base = create_cylinder(f"{name_prefix}_Base", base_radius, base_height, (location[0], location[1], location[2] + base_height / 2))
    tower_body = create_cylinder(f"{name_prefix}_Body", body_radius, body_height, (location[0], location[1], location[2] + base_height + body_height / 2))
    tower_top = create_cone(f"{name_prefix}_Top", top_radius, top_height, (location[0], location[1], location[2] + base_height + body_height + top_height / 2))
    
    tower_base_material = create_material("Tower_Base_Material", (0.8, 0.8, 0.8))
    tower_body_material = create_material("Tower_Body_Material", (0.2, 0.2, 0.2))  # Make the cylinder of the tower gray, closer to black
    tower_top_material = create_material("Tower_Top_Material", (1, 0, 0))  # Make the cone of the tower red
    
    tower_base.data.materials.append(tower_base_material)
    tower_body.data.materials.append(tower_body_material)
    tower_top.data.materials.append(tower_top_material)

def create_house(name_prefix, size, location):
    house_body = create_cube(f"{name_prefix}_Body", (size, size, size), (location[0], location[1], location[2] + size / 2))  # Move the cube up
    house_roof = create_pyramid(f"{name_prefix}_Roof", size, (location[0], location[1], location[2] + size + size / 2))  # Adjust the pyramid base size
    house_body_material = create_material("House_Body_Material", (0.9, 0.5, 0.2))
    house_roof_material = create_material("House_Roof_Material", (0.6, 0.3, 0.1))

    house_body.data.materials.append(house_body_material)
    house_roof.data.materials.append(house_roof_material)

def create_wall_ring(name, inner_radius, outer_radius, height, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=outer_radius, depth=height, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    outer_cylinder = bpy.context.active_object
    outer_cylinder.name = f"{name}_Outer"

    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=inner_radius, depth=height, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    inner_cylinder = bpy.context.active_object
    inner_cylinder.name = f"{name}_Inner"

    # Set the rotation
    outer_cylinder.rotation_axis_angle = (math.pi / 2, 1, 0, 0)
    inner_cylinder.rotation_axis_angle = (math.pi / 2, 1, 0, 0)

    # Perform the boolean operation
    mod = outer_cylinder.modifiers.new(name="Boolean_Difference", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.use_self = False
    mod.object = inner_cylinder
    bpy.context.view_layer.objects.active = outer_cylinder
    bpy.ops.object.modifier_apply({"object": outer_cylinder}, modifier=mod.name)

    # Delete the inner cylinder
    bpy.ops.object.select_all(action='DESELECT')
    inner_cylinder.select_set(True)
    bpy.ops.object.delete()
    wall_material = create_material("Wall_Material", (0.2, 0.2, 0.2))  # Make the wall the same color as the cylinder of the tower
    outer_cylinder.data.materials.append(wall_material)
    
def create_plane(name, size, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rotation
    plane_material = create_material("Ground_Plane_Material", (0.1, 0.5, 0.1))
    bpy.data.objects["Ground_Plane"].data.materials.append(plane_material)
    return obj

def create_door(name, size, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0], size[1], size[2])
    obj.rotation_euler = rotation
    return obj


def create_iron_door(name, size, location, wall_object):
    door = create_door(name, size, location)
    door_material = create_material("Iron_Door_Material", (0.5, 0.5, 0.5))  # Make the door look like iron
    door.data.materials.append(door_material)

    # Perform the boolean operation
    mod = wall_object.modifiers.new(name="Boolean_Difference_Door", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.use_self = False
    mod.object = door
    bpy.context.view_layer.objects.active = wall_object
    bpy.ops.object.modifier_apply({"object": wall_object}, modifier=mod.name)

    # Delete the door object used for the boolean operation
    bpy.ops.object.select_all(action='DESELECT')
    door.select_set(True)
    bpy.ops.object.delete()
    
# Delete all existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

#Create wall
wall_radius = 12
wall_height = 3
wall_thickness = 0.5
wall_angle_span = 10
wall_name = "Castle_Wall"
create_wall_ring(wall_name, wall_radius - wall_thickness / 2, wall_radius + wall_thickness / 2, wall_height, (0, 0, wall_height / 2), rotation=(math.pi / 2, 0, 0))

# Create corner towers
tower_radius = 1.5
tower_base_height = 0.5
tower_body_height = 5
tower_top_height = 2
for angle in range(0, 360, 90):
    rad_angle = math.radians(angle)
    x = (wall_radius - wall_thickness / 2) * math.cos(rad_angle)
    y = (wall_radius - wall_thickness / 2) * math.sin(rad_angle)
    create_tower(f"Corner_Tower_{angle}", tower_radius * 1.2, tower_base_height, tower_radius, tower_body_height, tower_radius * 1.5, tower_top_height, (x, y, 0))

# Create central castle
central_castle_radius = 3
central_castle_height = 7
create_tower("Central_Castle", central_castle_radius * 1.2, tower_base_height, central_castle_radius, central_castle_height, central_castle_radius * 1.5, tower_top_height, (0, 0, 0))

# Create village houses
house_count = 20
house_min_distance = wall_radius / 2
house_max_distance = wall_radius - 2
for i in range(house_count):
    angle = random.uniform(0, 360)
    distance = random.uniform(house_min_distance, house_max_distance)
    rad_angle = math.radians(angle)
    x = distance * math.cos(rad_angle)
    y = distance * math.sin(rad_angle)
    size = random.uniform(0.5, 1.5)
    create_house(f"House_{i}", size, (x, y, 0))

# Create ground plane
plane_size = 30
create_plane("Ground_Plane", plane_size, (0, 0, 0))

#Create an iron door in the wall
door_size = (1, wall_thickness, 2.5)  # Adjust the door size as needed
door_location = (0, wall_radius - wall_thickness / 2, door_size[2] / 2)  # Adjust the door location to be within the wall
wall_object = bpy.data.objects[wall_name + "_Outer"]
create_iron_door("Iron_Door", door_size, door_location, wall_object)
