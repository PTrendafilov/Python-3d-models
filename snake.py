import bpy
import math

def create_cylinder(name, radius, depth, location, rotation):
    bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=radius, depth=depth, end_fill_type='NGON', enter_editmode=False, align='WORLD', location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.rotation_euler = rotation
    return obj

# Delete all existing mesh objects
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Parameters for the snake
segment_count = 50
segment_length = 0.5
segment_radius = 0.25
snake_length = segment_count * segment_length

# Create the snake segments
for i in range(segment_count):
    x = i * segment_length
    y = 0
    z = math.sin(x / snake_length * 2 * math.pi) * segment_length * 2
    location = (x, y, z)
    rotation = (math.pi / 2, 0, 0)
    create_cylinder(f"Snake_Segment_{i}", segment_radius, segment_length, location, rotation)
