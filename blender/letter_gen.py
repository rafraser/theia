import argparse, bpy, math, mathutils, os, sys


def cleanup_scene():
    """Cleanup the initial scene
    This will remove everything in the initial collection

    If you have a totally blank startup file, you'll want to remove this bit
    """
    bpy.data.collections.remove(bpy.data.collections[0])


def set_source_export(folder="output"):
    """Set the export directory for the Blender Source Tools plugin

    Args:
        folder (str, optional): Export path, relative to working directory. Defaults to "output".
    """
    bpy.context.scene.vs.export_format = "SMD"
    bpy.context.scene.vs.export_path = os.path.join(os.getcwd(), folder)


def add_text(
    font="C:\\Windows\\Fonts\\Roboto-Bold.ttf",
    text="A",
    size=100,
    offset=0,
    extrude=0.1,
    primary_material_name="letter_primary",
    secondary_material_name="letter_red",
    quality=4,
):
    """[summary]

    Args:
        font (str, optional): Path to a font file. Defaults to "C:\Windows\Fonts\Roboto-Bold.ttf".
        text (str, optional): Text to render. Defaults to "A".
        size (int, optional): Size for the resulting text. Defaults to 100.
        offset (int, optional): Offset?. Defaults to 0.
        extrude (float, optional): Depth for the 3D text. Defaults to 0.1.
        primary_material_name (str, optional): Texture name to use for the primary material. Defaults to "letter_primary".
        secondary_material_name (str, optional): Texture name to use for the front face material. Defaults to "letter_red".
        quality (int, optional): Quality to use when remeshing the text. Defaults to 4. Increase for more complicated fonts.
    """
    # Create a new collection for this object
    new_collection = bpy.data.collections.new(text)
    bpy.context.scene.collection.children.link(new_collection)

    # Create the object
    bpy.ops.object.text_add(
        enter_editmode=False,
        align="WORLD",
        location=(0, 0, 0),
        scale=(size, size, size),
    )
    ob = bpy.context.active_object
    ob.scale = (size, size, size)

    # Handle collections and selection
    old_collections = ob.users_collection
    new_collection.objects.link(ob)
    for old_collection in old_collections:
        old_collection.objects.unlink(ob)
    ob.select_set(True)

    # Handle properties
    ob.rotation_euler[0] = math.radians(90)
    ob.data.align_x = "CENTER"
    ob.data.align_y = "BOTTOM_BASELINE"
    ob.data.body = text
    ob.data.font = bpy.data.fonts.load(font)
    ob.data.offset = offset
    ob.data.extrude = extrude

    # Helper stuff
    convert_text_to_mesh(ob, quality)
    apply_text_materials(ob, primary_material_name, secondary_material_name)


def convert_text_to_mesh(ob, quality):
    """Convert a text curve to a mesh object


    Args:
        ob: Text curve to convert to mesh
        quality: Octree depth for the remesh modifier
    """
    # Setup remesh modifier first
    bpy.ops.object.modifier_add(type="REMESH")
    ob.modifiers["Remesh"].mode = "SHARP"
    ob.modifiers["Remesh"].use_remove_disconnected = False
    ob.modifiers["Remesh"].octree_depth = quality

    # Convert to mesh
    bpy.ops.object.convert(target="MESH")


def apply_text_materials(ob, primary_material_name, secondary_material_name):
    """Apply the materials to the text object
    The primary material is used for the 'base' of the text
    The secondary material is applied to the 'front' of the text

    Args:
        ob: Mesh to apply materials to
        primary_material_name: Material name for primary material
        secondary_material_name: Material name for front facing material
    """
    # Setup the materials
    # The names are really only used for the textures later on
    # Make double sure that the names are correct
    primary_mat = bpy.data.materials.new(name=primary_material_name)
    ob.data.materials.append(primary_mat)
    ob.active_material_index = 0
    ob.active_material.name = primary_material_name
    secondary_mat = bpy.data.materials.new(name=secondary_material_name)
    ob.data.materials.append(secondary_mat)
    ob.active_material_index = 1
    ob.active_material.name = secondary_material_name
    ob.active_material.diffuse_color = (1, 0, 0, 1)

    # Apply the secondary material to only front-facing faces
    for face in ob.data.polygons:
        if face.normal == mathutils.Vector((0, 0, 1)):
            face.material_index = 1


def export_collection_to_smd(cleanup=True):
    """Export the main collection to an SMD

    Args:
        cleanup (bool, optional): Whether to remove the collection afterwards. Defaults to True.
    """
    bpy.ops.export_scene.smd(collection="", export_scene=False)

    # Delete the collection if requested
    # i'm pretty sure this keeps the object in memory but oh well
    if cleanup:
        collection = bpy.data.collections[0]
        bpy.data.collections.remove(collection)


def generate_letter(string, args):
    """Generate a single 3D text object

    Args:
        string (str): Text to generate
        args: other arguments - see argparser below
    """
    add_text(text=string, font=args.font, quality=args.quality, extrude=args.extrude)
    export_collection_to_smd(cleanup=True)


if __name__ == "__main__":
    # will document these parameters later
    # for an example of this script, see the Letter Set project script
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--characters", default="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    parser.add_argument("--font", default="C:\\Windows\\Fonts\\Roboto-Bold.ttf")
    parser.add_argument("--quality", default=4, type=int)
    parser.add_argument("--extrude", default=0.05, type=float)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])

    cleanup_scene()
    set_source_export(folder=args.output)
    for char in args.characters:
        generate_letter(char, args)
