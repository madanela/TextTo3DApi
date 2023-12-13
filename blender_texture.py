import bpy

# Constants
OBJ_FILE_PATH = "./example_mesh_0.obj"
OUTPUT_IMAGE_PATH = "./example_mesh_0.png"
USDZ_FILE_PATH = "./example_mesh_0.usdz"
MATERIAL_NAME = "Gevor"

def import_obj(filepath):
    bpy.ops.wm.obj_import(filepath=filepath)

def setup_material(material_name):
    if material_name not in bpy.data.materials:
        mat = bpy.data.materials.new(name=material_name)
    else:
        mat = bpy.data.materials[material_name]
    return mat

def uv_unwrap():
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project()
    bpy.ops.object.mode_set(mode='OBJECT')

def bake_diffuse(material):
    bpy.context.object.active_material = material
    bpy.ops.object.bake(type='DIFFUSE')

def save_image(image_name, filepath):
    image = bpy.data.images.get(image_name)
    if image:
        image.save_render(filepath)

def export_usdz(filepath, filter=None):
    if filter:
        for obj in bpy.context.scene.objects:
            obj.select_set(False)
        filter.select_set(True)
        bpy.context.view_layer.objects.active = filter
    bpy.ops.wm.usd_export(filepath=filepath, check_existing=False, selected_objects_only=bool(filter))

def cleanup_and_exit():
    bpy.ops.wm.quit_blender()


# Import the OBJ file
import_obj(OBJ_FILE_PATH)

# Set up the material
material = setup_material(MATERIAL_NAME)

# UV unwrap
uv_unwrap()

# Bake the diffuse texture
bake_diffuse(material)

# Save the baked image
# The name of the image can vary, so we try to dynamically get it
baked_image_name = next((img.name for img in bpy.data.images if "Render Result" not in img.name), None)
if baked_image_name:
    save_image(baked_image_name, OUTPUT_IMAGE_PATH)

# Export to USDZ format
export_usdz(USDZ_FILE_PATH)

# Cleanup and exit Blender
cleanup_and_exit()