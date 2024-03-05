import bpy
import math

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    return r, g, b

def rgb2hsv(r, g, b):
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

# # Delete all existing mesh objects
# bpy.ops.object.select_all(action='DESELECT')
# bpy.ops.object.select_by_type(type='MESH')
# bpy.ops.object.delete()

# # # Delete all existing materials
# # bpy.ops.material.select_all(action='DESELECT')
# # bpy.ops.material.delete()

# # Delete the existing camera
# bpy.ops.object.select_by_type(type='CAMERA')
# bpy.ops.object.delete()

# Delete all existing mesh objects
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

# Delete all existing materials
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat, do_unlink=True)

# Delete the existing camera
for cam in bpy.data.cameras:
    bpy.data.cameras.remove(cam, do_unlink=True)

# Add a new camera
bpy.ops.object.camera_add(location=(0, 0, 0))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

# Set camera movement keyframes
camera_keyframes = [
    {"frame": 0, "location": (3.89864 , -2.99435, 5.55246 )}]

for keyframe in camera_keyframes:
    bpy.context.scene.frame_set(keyframe["frame"])
    camera.location = keyframe["location"]
    camera.keyframe_insert(data_path="location", frame=keyframe["frame"])

# Add an empty cube
bpy.ops.object.empty_add(type='CUBE')
cube_empty = bpy.context.active_object
cube_empty.location = (-1.26726, 0.31629, 0.8773) 

camera.constraints.new(type='TRACK_TO')
camera.constraints['Track To'].target = cube_empty
camera.constraints['Track To'].up_axis = 'UP_Y'
camera.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
camera.data.lens = 35.26

# # Add light source
# bpy.ops.object.light_add(type='SUN', location=(6.8018, 4.7748, 5))
# light = bpy.context.active_object
# light.data.energy = 2

bpy.ops.object.light_add(type='AREA', location=(-1.38627, 0.371628, 5))
light = bpy.context.active_object
light.data.energy = 1800
light.data.size = 15
bpy.context.object.data.color = (0.977826, 1, 0.844369)

# Load the human OBJ files at different frames

human_frame = [55, 106, 70, 80, 206, 300, 60, 957, 468, 30, 65, 349]
motion_file = ['motion_multiobj_seq', 'motion_cabinet', 'motion_multiobj_seq', 'motion_multiobj_seq', 'motion_multiobj_seq', 'motion_multiobj_seq',
            'motion_multiobj_seq', 'back_relax', 'multiobj_sit_seq', 'motion_multiobj_seq',
            'motion_multiobj_seq', 'multiobj_bed_seq']

frame_num = len(human_frame)

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = frame_num



h, s, v = rgb2hsv(0.022968, 0.55378, 0.8)
for idx, frame_to_show in enumerate(human_frame):
    bpy.ops.import_scene.obj(filepath="/home/zqxiao/xml2mesh-main/"+motion_file[idx]+"/full_body"+str(frame_to_show)+".obj")
    human_obj = bpy.context.selected_objects[0]
    if frame_to_show == 300:
        human_obj.rotation_euler = (0, 0, 0)
        human_obj.location = (0.124873, 2.37256, 0)
        ss = 0.6
    elif frame_to_show == 50:
        human_obj.rotation_euler = (0, 0, -85/180*3.1415924535)
        human_obj.location = (-0.061344, -1.00438, 0)
        ss = 0.6
    elif frame_to_show == 60:
        human_obj.rotation_euler = (0, 0, -90/180*3.1415924535)
        human_obj.location = (0.239471, -1.00714, 0)
        ss = 0.6
    elif frame_to_show == 70:
        human_obj.rotation_euler = (0, 0, 40/180*3.1415924535)
        human_obj.location = (-0.986875, 2.74349, 0)
        ss = 0.6
    elif frame_to_show == 80:
        human_obj.rotation_euler = (0, 0, 0)
        human_obj.location = (0, 3, 0)
        ss = 0.6
    elif frame_to_show == 206:
        human_obj.rotation_euler = (0, 0, 0)
        human_obj.location = (0, 3, 0)
        ss = 1
    elif frame_to_show == 957:
        human_obj.rotation_euler = (0, -10/180*3.1415924535, -45/180*3.1415924535)
        human_obj.location = (0.498487, 0.277122, -0.072577)
        ss = 1
    elif frame_to_show == 468:
        human_obj.rotation_euler = (0, 10/180*3.1415924535, -45/180*3.1415924535)
        human_obj.location = (-0.758808, -0.192137 , 0.152881)
        ss = 1
    elif frame_to_show == 106:
        human_obj.rotation_euler = (0, 10/180*3.1415924535, -180/180*3.1415924535)
        human_obj.location = (-0.620735, 7.244, 0.152881)
        ss = 1
    elif frame_to_show == 349:
        human_obj.rotation_euler = (0, 0, -90/180*3.1415924535)
        human_obj.location = (-2.81679, -0.016173, 0.021243)
        ss = 1
    elif frame_to_show == 30:
        human_obj.rotation_euler = (0, 0, -200/180*3.1415924535)
        human_obj.location = (-4.55247, -0.553077, 0.001481)
        ss = 0.6
    elif frame_to_show == 40:
        human_obj.rotation_euler = (0, 0, 90/180*3.1415924535)
        human_obj.location = (-2.56929, 2.44053, 0.01363)
        ss = 0.6
    elif frame_to_show == 55:
        human_obj.rotation_euler = (0, 0, 90/180*3.1415924535)
        human_obj.location = (-2.19655, 2.14915, -0.020505)
        ss = 0.6
    elif frame_to_show == 65:
        human_obj.rotation_euler = (0, 0, -200/180*3.1415924535)
        human_obj.location = (-3.70505, -1.74358, 0.001884)
        ss = 0.6

    # if frame_to_show == 468:
    #     r,g,b = (1, 0.707593, 0.0402351)
    # else:
    r,g,b = hsv2rgb(h,ss,v)
    if idx == 0:
        bpy.data.materials["Default OBJ"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r,g,b,1)
    else:
        bpy.data.materials["Default OBJ."+str(idx).zfill(3)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (r,g,b,1)

    for fn in range(frame_num):
        human_obj.hide_viewport = fn < idx
        human_obj.hide_render = fn < idx
        human_obj.keyframe_insert(data_path="hide_viewport", frame=fn)
        human_obj.keyframe_insert(data_path="hide_render", frame=fn)
        human_obj.keyframe_insert(data_path="location", frame=fn)
        human_obj.keyframe_insert(data_path="rotation_euler", frame=fn)

# scene 1
# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/46703/models/model_normalized.obj" # cabinet
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 200/180*3.1415924535)  # Replace rx, ry, rz with rotation values
obj_object.location = (-1.87745,2.65296,1.19579)  # Replace x, y, z with location values
obj_object.scale = (2.5, 2.5, 2.5)
obj_object.keyframe_insert(data_path="scale", frame=0)

# scene 2
# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/37825/models/model_normalized.obj" # chair
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, -1.5707963267948966)  # Replace rx, ry, rz with rotation values
obj_object.location = (0.016415,1,0.329635)  # Replace x, y, z with location values
obj_object.scale = (1.2, 1.5, 1.2)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/11873/models/model_normalized.obj" # laptop
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 1.5707963267948966)  # Replace rx, ry, rz with rotation values
obj_object.location = (0.83648,1.05432,0.738129)  # Replace x, y, z with location values
obj_object.scale = (0.6, 0.6, 0.6)
obj_object.keyframe_insert(data_path="scale", frame=0)


# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/21980/models/model_normalized.obj" # table
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 1.5707963267948966)  # Replace rx, ry, rz with rotation values
obj_object.location = (1.08839,1,0.392069)  # Replace x, y, z with location values
obj_object.scale = (1.8, 2.0, 1.8)
obj_object.keyframe_insert(data_path="scale", frame=0)
# obj_object.keyframe_insert(data_path="location", frame=0)

# scene 3

# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/37700/models/model_normalized.obj" # chair
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, -135/180*3.1415924535)  # Replace rx, ry, rz with rotation values
obj_object.location = (-1.25901,-1.00284,0.42955)  # Replace x, y, z with location values
obj_object.scale = (1.2, 1.5, 1.2)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/37700/models/model_normalized.obj" # chair
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, -135/180*3.1415924535)  # Replace rx, ry, rz with rotation values
obj_object.location = (-1.87875,-1.62961,0.42955)  # Replace x, y, z with location values
obj_object.scale = (1.2, 1.5, 1.2)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/5411/models/model_normalized.obj" # screen
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 45/180*3.1415924535)  # Replace rx, ry, rz with rotation values
obj_object.location = (-0.551736,-2.18358,0.447505)  # Replace x, y, z with location values
obj_object.scale = (1.2, 1.2, 1.2)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/24992/models/model_normalized.obj" # table
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 45/180*3.1415924535)  # Replace rx, ry, rz with rotation values
obj_object.location = (-0.478118,-2.21341,0.153963)  # Replace x, y, z with location values
obj_object.scale = (1.0, 1.0, 1.0)
obj_object.keyframe_insert(data_path="scale", frame=0)

# scene 4
# Import OBJ file
ply_file_path = "/home/zqxiao/ASE_private/partnet_sample/12032/models/model_normalized.obj" # bed
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 3.1415924535)  # Replace rx, ry, rz with rotation values
obj_object.location = (-4.61813, -0.049981, 0.567497)  # Replace x, y, z with location values
obj_object.scale = (3, 3, 3)
obj_object.keyframe_insert(data_path="scale", frame=0)

wood_texture = bpy.data.images.load("/home/zqxiao/blender/floor.png")  # Replace with your wood texture path
wall_texture = bpy.data.images.load("/home/zqxiao/blender/wall_texture.jpg")  # Replace with your wood texture path
# wood_texture = wall_texture

for i in range(8):
    for j in range(8):
        # Create a wooden floor mesh
        bpy.ops.mesh.primitive_plane_add(size=2)
        floor = bpy.context.active_object
        floor.location = (i*2-3-4-5, j*2-1.5-3+1, 0)

        # Create a material for the wooden floor
        floor_material = bpy.data.materials.new(name="WoodenFloor")
        floor.data.materials.append(floor_material)
        floor.active_material = floor_material

        # Assign a wood texture to the material
        floor_material.use_nodes = True
        nodes = floor_material.node_tree.nodes
        node_tree = floor_material.node_tree

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)

        # Create texture node
        texture_node = nodes.new(type='ShaderNodeTexImage')
        texture_node.image = wood_texture
        texture_coord = nodes.new(type='ShaderNodeTexCoord')
        mapping_node = nodes.new(type='ShaderNodeMapping')
        mapping_node.vector_type = 'TEXTURE'
        diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')

        # Link nodes
        links = node_tree.links
        links.new(texture_node.outputs['Color'], diffuse_node.inputs['Color'])
        links.new(mapping_node.outputs['Vector'], texture_node.inputs['Vector'])
        links.new(texture_coord.outputs['UV'], mapping_node.inputs['Vector'])

        # Set up material output node
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        links.new(diffuse_node.outputs['BSDF'], output_node.inputs['Surface'])

# Set rendering settings
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = "teaser_gif/"
bpy.context.scene.cycles.samples = 64
bpy.context.scene.cycles.use_denoising = True

# Render the animation
bpy.ops.render.render(animation=True)