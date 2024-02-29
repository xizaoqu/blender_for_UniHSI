import bpy

# Delete all existing mesh objects
for obj in bpy.data.objects:
    bpy.data.objects.remove(obj, do_unlink=True)

# Delete all existing materials
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat, do_unlink=True)

# Delete the existing camera
for cam in bpy.data.cameras:
    bpy.data.cameras.remove(cam, do_unlink=True)

# Import OBJ file
ply_file_path = "assets/objects/40399/models/model_normalized.obj" # chair 1
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, -1.5707963267948966)  # Replace rx, ry, rz with rotation values
obj_object.location = (1.2132,-0.437862,0.408171)  # Replace x, y, z with location values
obj_object.scale = (1.2, 1.3, 1.2)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Import OBJ file
ply_file_path = "assets/objects/34684/models/model_normalized.obj" # table 1
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 1.5707963267948966)  # Replace rx, ry, rz with rotation values
obj_object.location = (2.22503,-0.616297,0.277157)  # Replace x, y, z with location values
obj_object.scale = (1.8, 1.8, 1.8)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Import OBJ file
ply_file_path = "assets/objects/37738/models/model_normalized.obj" # chair 2
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, -1.5707963267948966)  # Replace rx, ry, rz with rotation values
obj_object.location = ([-0.302647,-2.10163,0.389669])  # Replace x, y, z with location values
obj_object.scale = (1.2, 1.2, 1.2)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Import OBJ file
ply_file_path = "assets/objects/4376/models/model_normalized.obj" # vase
bpy.ops.import_scene.obj(filepath=ply_file_path)

# Access the imported object
obj_object = bpy.context.selected_objects[0]
obj_mesh = obj_object.data
obj_object.rotation_euler = (1.5707963267948966, 0, 1.5707963267948966)  # Replace rx, ry, rz with rotation values
obj_object.location = (-0.437887,-2.53024,0.38491)  # Replace x, y, z with location values
obj_object.scale = (0.5, 0.93, 0.5)
obj_object.keyframe_insert(data_path="scale", frame=0)

# Add a new camera
bpy.ops.object.camera_add(location=(0, 0, 0))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

camera_keyframes = [
    {"frame": 0, "location": (-0.493389, -5.48486 , 3.30533)}]

for keyframe in camera_keyframes:
    bpy.context.scene.frame_set(keyframe["frame"])
    camera.location = keyframe["location"]
    camera.keyframe_insert(data_path="location", frame=keyframe["frame"])

# Add an empty cube
bpy.ops.object.empty_add(type='CUBE')
cube_empty = bpy.context.active_object
cube_empty.location = (1.01024, -2.29449, 0.8773) 

camera.constraints.new(type='TRACK_TO')
camera.constraints['Track To'].target = cube_empty
camera.constraints['Track To'].up_axis = 'UP_Y'
camera.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
camera.data.lens = 35.26

bpy.ops.object.light_add(type='AREA', location=(1.0039, -1.9812, 5))
light = bpy.context.active_object
light.data.energy = 500
light.data.size = 5

# Load the human OBJ files at different frames

human_number = 1

bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = human_number -1 


for frame_to_show in range(human_number):
    bpy.ops.import_scene.obj(filepath="assets/human_body/multiobj_multistep_2/full_body"+str(frame_to_show)+".obj")
    human_obj = bpy.context.selected_objects[0]
    human_obj.rotation_euler = (0, 0, 0)
    human_obj.location = (0, 0, 0)
    # human_obj.location = (0, frame_to_show, 0)  # Replace x, y, z with location values
    
    for frame_num in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end + 1):
        human_obj.hide_viewport = frame_num != frame_to_show
        human_obj.hide_render = frame_num != frame_to_show
        human_obj.keyframe_insert(data_path="hide_viewport", frame=frame_num)
        human_obj.keyframe_insert(data_path="hide_render", frame=frame_num)
        human_obj.keyframe_insert(data_path="location", frame=frame_num)
        human_obj.keyframe_insert(data_path="rotation_euler", frame=frame_num)
    if frame_to_show == 0:
        bpy.data.materials["Default OBJ"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.141157, 1, 0.141026, 1)
    else:
        bpy.data.materials["Default OBJ."+str(frame_to_show).zfill(3)].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.141157, 1, 0.141026, 1)

wall_texture = bpy.data.images.load("assets/wall_texture.jpg")  # Replace with your texture path


for i in range(8):
    for j in range(8):
        # Create a wooden floor mesh
        bpy.ops.mesh.primitive_plane_add(size=2)
        floor = bpy.context.active_object
        floor.location = (i*2-3-4, j*2-1.5-3-4, 0)

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
        texture_node.image = wall_texture
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
bpy.context.scene.render.filepath = "output_multiobj_multistep_2/"
bpy.context.scene.cycles.samples = 16
bpy.context.scene.cycles.use_denoising = True

# Render the animation
bpy.ops.render.render(animation=True)