"""Render the landing's conceptual neighborhood with Blender 5 (no external assets).

blender -b -t 6 --python scripts/render-neighborhood.py -- --output /tmp/neighborhood.png
The PNG is a render intermediate; publish a WebP in assets/images/.
"""
import argparse
import math
import sys

import bpy
from mathutils import Vector


def material(name, color, roughness=0.7, metallic=0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1)
    mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Metallic'].default_value = metallic
    return mat


def box(name, location, size, mat, bevel=0.04):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    if bevel:
        modifier = obj.modifiers.new('Soft edges', 'BEVEL')
        modifier.width = bevel
        modifier.segments = 3
        obj.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    return obj


def cylinder(name, location, radius, depth, mat):
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new('Soft edge', 'BEVEL')
    bevel.width = 0.04
    bevel.segments = 3
    obj.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    return obj


def tree(x, y, scale=1):
    cylinder('Tree planter', (x, y, .30), .36 * scale, .22, cream)
    cylinder('Tree trunk', (x, y, .77 * scale), .055 * scale, 1.0 * scale, wood)
    for dx, dy, z, radius in [(0, 0, 1.50, .53), (-.20, .03, 1.23, .37), (.22, .06, 1.35, .40)]:
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=radius * scale,
                                            location=(x + dx * scale, y + dy * scale, z * scale))
        obj = bpy.context.object
        obj.name = 'Sculpted foliage'
        obj.scale = (.88, .88, 1.1)
        obj.data.materials.append(sage)
        for face in obj.data.polygons:
            face.use_smooth = True


def neighbor(x, y, width, depth, height, mat):
    box('Neighborhood building', (x, y, .20 + height / 2), (width, depth, height), mat, .065)
    box('Flat roof edge', (x, y, .24 + height), (width + .13, depth + .13, .17), cream)
    for z in [1.0, 2.2, 3.4]:
        if z < height - .2:
            for dx in [-width * .24, width * .24]:
                box('Window recess', (x + dx, y - depth / 2 - .015, z), (.45, .04, .66), stone)
                box('Window glass', (x + dx, y - depth / 2 - .04, z), (.34, .025, .54), glass)
                box('Window sill', (x + dx, y - depth / 2 - .09, z - .33), (.49, .20, .06), cream)


args = argparse.ArgumentParser()
args.add_argument('--output', required=True)
options = args.parse_args(sys.argv[sys.argv.index('--') + 1:])
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

cream = material('Warm porcelain', (.83, .81, .72))
ivory = material('Ivory plaster', (.72, .73, .64))
stone = material('Limestone', (.50, .57, .50))
road = material('Pale stone paving', (.68, .72, .67))
paper = material('Platform edge', (.85, .86, .79))
teal = material('Deep green storefront', (.026, .23, .17))
mint = material('Mint route', (.28, .67, .49))
sage = material('Sage foliage', (.27, .43, .30))
glass = material('Muted glass', (.18, .31, .29), .27, .12)
wood = material('Natural oak', (.47, .32, .18))
brass = material('Brass details', (.68, .49, .22), .32, .4)

box('Neighborhood plinth', (0, 0, -.035), (8.2, 6.5, .38), paper, .18)
box('Walking street', (0, -1.90, .168), (7.9, 1.90, .06), road, .05)
box('Back sidewalk', (0, .98, .20), (7.9, 3.75, .15), ivory, .04)
for x in range(-3, 4):
    box('Paving seam', (x, -1.9, .204), (.012, 1.80, .004), stone, 0)
box('Paving seam', (0, -1.9, .205), (7.8, .012, .004), stone, 0)

neighbor(-2.30, 1.45, 2.15, 2.10, 3.7, ivory)
neighbor(2.65, 1.95, 1.70, 1.8, 3.0, cream)

# Main storefront faces the walking street.
box('Chosen shop', (.50, .35, 1.43), (2.75, 2.35, 2.45), cream, .055)
box('Green storefront frame', (.50, -.855, 1.10), (2.73, .11, 1.79), teal, .035)
box('Shop window', (.12, -.927, 1.03), (1.45, .035, 1.39), glass, .025)
box('Glass door', (1.17, -.93, 1.02), (.57, .04, 1.48), glass, .02)
box('Door handle', (1.34, -.985, 1.05), (.028, .045, .25), brass, .012)
box('Window crossbar', (.12, -.96, 1.03), (.028, .025, 1.40), teal, .008)
box('Shop sign', (.50, -.94, 2.12), (2.76, .18, .40), teal, .025)
for n in range(9):
    awning = box('Striped canvas awning', (-.735 + n * .309, -1.08, 1.86),
                 (.305, .68, .105), cream if n % 2 else teal, .014)
    awning.rotation_euler[0] = math.radians(12)
    box('Awning valance', (-.735 + n * .309, -1.409, 1.73),
        (.305, .04, .19), cream if n % 2 else teal, .025)
box('Shop roof cap', (.50, .35, 2.70), (2.94, 2.55, .19), cream, .055)
box('Roof terrace', (.50, .40, 2.82), (2.36, 1.95, .10), stone, .04)
box('Roof parapet back', (.50, 1.56, 2.94), (2.84, .13, .40), cream)
box('Roof parapet side', (-.91, .37, 2.94), (.13, 2.42, .40), cream)

# Mint inlay leads to the selected shop; it is a conceptual route, not map data.
box('Mint route horizontal', (-1.0, -2.43, .216), (4.2, .095, .012), mint, .04)
box('Mint route toward shop', (1.08, -1.90, .218), (.095, 1.13, .012), mint, .04)
cylinder('Route start', (-3.08, -2.43, .223), .14, .026, teal)
cylinder('Route stop', (1.08, -1.36, .223), .14, .026, mint)

# A floating map pin above the roof, turned to face the camera.
bpy.ops.mesh.primitive_torus_add(major_segments=64, minor_segments=20,
    location=(.50, .38, 3.71), major_radius=.34, minor_radius=.10,
    rotation=(math.pi / 2, 0, math.radians(29)))
pin = bpy.context.object
pin.name = 'Selected location pin'
pin.data.materials.append(teal)
for face in pin.data.polygons:
    face.use_smooth = True
bpy.ops.mesh.primitive_cone_add(vertices=4, radius1=0, radius2=.21, depth=.37,
    location=(.50, .38, 3.30), rotation=(0, 0, math.radians(29)))
bpy.context.object.data.materials.append(teal)

tree(-3.12, -.60, .92)
tree(3.16, -.42, .98)
tree(-3.23, 2.52, .82)
for x in [-2.03, 2.49]:
    box('Bench seat', (x, -1.05, .55), (.85, .28, .11), wood)
    for dx in [-.29, .29]:
        box('Bench leg', (x + dx, -1.05, .37), (.065, .22, .31), teal, .015)
cylinder('Shop planter', (-.58, -1.52, .36), .18, .31, cream)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=12, radius=.24, location=(-.58, -1.52, .67))
bpy.context.object.data.materials.append(sage)

scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.cycles.device = 'CPU'
scene.cycles.samples = 48
scene.cycles.use_denoising = True
scene.render.resolution_x = 1200
scene.render.resolution_y = 1050
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.film_transparent = True
scene.render.filepath = options.output
scene.world.color = (.65, .65, .65)
scene.view_settings.view_transform = 'AgX'

for name, location, power, size in [('Large softbox', (-4, -6, 11), 1500, 7), ('Fill', (6, 1, 8), 800, 6)]:
    bpy.ops.object.light_add(type='AREA', location=location)
    light = bpy.context.object
    light.name = name
    light.data.energy = power
    light.data.shape = 'DISK'
    light.data.size = size
    light.rotation_euler = (Vector((0, 0, 1)) - light.location).to_track_quat('-Z', 'Y').to_euler()
bpy.ops.object.camera_add(location=(10, -14, 12))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, 1.1)) - camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 11.6
scene.camera = camera
scene.render.image_settings.color_depth = '8'
bpy.ops.render.render(write_still=True)
