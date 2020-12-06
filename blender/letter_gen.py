import bpy
import math, os


def remove_cube():
    bpy.data.objects["Cube"].select_set(True)
    bpy.ops.object.delete()


def set_source_export(folder="output"):
    bpy.context.scene.vs.export_format = "SMD"
    bpy.context.scene.vs.export_path = os.path.join(os.getcwd(), folder)


def add_text(
    font="C:\\Windows\\Fonts\\Roboto-Bold.ttf",
    text="Hello World!",
    size=1,
    offset=0,
    extrude=0.1,
    bevel=0.01,
):
    bpy.ops.object.text_add(
        enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
    )
    ob = bpy.data.objects["Text"]
    ob.data.align_x = "CENTER"
    ob.data.align_y = "BOTTOM_BASELINE"
    ob.rotation_euler[0] = math.radians(90)

    ob.data.body = text
    ob.data.font = bpy.data.fonts.load(font)
    ob.data.offset = offset
    ob.data.extrude = extrude
    ob.data.bevel_depth = bevel


def export_collection_to_smd(name="Test Collection 1"):
    collection = bpy.data.collections[0]
    collection.name = name
    bpy.ops.export_scene.smd(collection="", export_scene=False)


if __name__ == "__main__":
    text = "Hello World"
    remove_cube()
    set_source_export()
    add_text(text=text)
    export_collection_to_smd(name=text)
