import bpy
import math, os, mathutils


def cleanup_scene():
    # Remove the initial scene stuff
    bpy.data.collections.remove(bpy.data.collections[0])


def set_source_export(folder="output"):
    bpy.context.scene.vs.export_format = "SMD"
    bpy.context.scene.vs.export_path = os.path.join(os.getcwd(), folder)


def add_text(
    font="C:\\Windows\\Fonts\\Roboto-Bold.ttf",
    text="Hello World!",
    size=1,
    offset=0,
    extrude=0.1,
    primary_material_name="white",
    secondary_material_name="blue",
):
    # Create a new collection for this object
    collection = bpy.data.collections.new(text)
    bpy.context.scene.collection.children.link(collection)

    # Create the object
    bpy.ops.object.text_add(
        enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
    )
    ob = bpy.data.objects["Text"]
    ob.data.align_x = "CENTER"
    ob.data.align_y = "BOTTOM_BASELINE"
    ob.rotation_euler[0] = math.radians(90)

    old_collections = ob.users_collection
    collection.objects.link(ob)
    for old_collection in old_collections:
        old_collection.objects.unlink(ob)

    ob.data.body = text
    ob.data.font = bpy.data.fonts.load(font)
    ob.data.offset = offset
    ob.data.extrude = extrude

    # Helper stuff
    convert_text_to_mesh(ob)
    apply_text_materials(ob, primary_material_name, secondary_material_name)


def convert_text_to_mesh(ob):
    # Setup remesh modifier first
    bpy.ops.object.modifier_add(type="REMESH")
    ob.modifiers["Remesh"].mode = "SHARP"
    ob.modifiers["Remesh"].use_remove_disconnected = False
    ob.modifiers["Remesh"].octree_depth = 7

    # Convert to mesh
    bpy.ops.object.convert(target="MESH")


def apply_text_materials(ob, primary_material_name, secondary_material_name):
    # Setup the materials
    # We only care about the names in Blender
    primary_mat = bpy.data.materials.new(name=primary_material_name)
    ob.data.materials.append(primary_mat)
    secondary_mat = bpy.data.materials.new(name=secondary_material_name)
    ob.data.materials.append(secondary_mat)
    ob.active_material_index = 1
    ob.active_material.diffuse_color = (1, 0, 0, 1)

    # Apply the secondary material to only front-facing faces
    for face in ob.data.polygons:
        if face.normal == mathutils.Vector((0, 0, 1)):
            face.material_index = 1


def export_collection_to_smd(cleanup=True):
    bpy.ops.export_scene.smd(collection="", export_scene=False)

    if cleanup:
        bpy.data.collections.remove(collection)


if __name__ == "__main__":
    text = "Hello World"
    cleanup_scene()
    set_source_export()
    add_text(text=text)
    export_collection_to_smd(name=text)
