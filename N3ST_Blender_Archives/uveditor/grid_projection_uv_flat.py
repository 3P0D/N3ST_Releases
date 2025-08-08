import bpy
import os
import bmesh  
import bpy.utils.previews  
preview_col = None  
def clear_previews():
    global preview_col  
    if preview_col is not None:  
        bpy.utils.previews.remove(preview_col)  
        preview_col = None  
def make_preview_icon(filepath):
    global preview_col  
    if preview_col is None:  
        preview_col = bpy.utils.previews.new()  
    icon_name = os.path.basename(filepath)  
    if icon_name not in preview_col:  
        preview_col.load(icon_name, filepath, 'IMAGE')  
    return preview_col[icon_name].icon_id  
def create_color_square_image(color, filename, folder):
    width, height = 8, 8  
    os.makedirs(folder, exist_ok=True)  
    path = os.path.join(folder, filename)  
    if os.path.exists(path):
        return path  
    image = bpy.data.images.new(name=filename, width=width, height=height, alpha=True)  
    pixels = list(color) * (width * height)  
    image.pixels = pixels  
    image.file_format = 'PNG'  
    image.filepath_raw = path  
    image.save()  
    bpy.data.images.remove(image)  
    return path  
def get_image(image):
    if image is None:  
        print("N3ST: No selected image(s).")  
        return None  
    if image.pixels:  
        return image  
    else: 
        print(f"Image {image.name} sans pixels")  
        return None  
def center_cell_pixel_color(image, row, col, n_rows, n_cols):
    if not image or not image.pixels:  
        return (1, 1, 1, 1)  
    w, h = image.size  
    x = int((col + 0.5) / n_cols * w)  
    y = int((row + 0.5) / n_rows * h)  
    x = max(0, min(w - 1, x))  
    y = max(0, min(h - 1, y))  
    idx = (y * w + x) * image.channels  
    px = image.pixels  
    if idx + 3 >= len(px):  
        return (1, 1, 1, 1)  
    return tuple(px[idx:idx + 4])  
class N3ST_UVEDIT_PROP_color_item(bpy.types.PropertyGroup):
    color: bpy.props.FloatVectorProperty(
        name="Color Picker",  
        subtype='COLOR',  
        size=4,  
        min=0.0, max=1.0,  
        default=(1, 1, 1, 1)  
    )  
    icon_path: bpy.props.StringProperty(name="Icon path") 
class N3ST_UVEDIT_OP_fill_color_grid(bpy.types.Operator):
    bl_idname = "n3st_uvedit.fill_color_grid"
    bl_label = "Generate icons and fill the grid"
    bl_description = ("Generate the image textures from the loaded image and fill the grid. "
                      "WARNING! Will create a folder named where your file was last saved and save the icons within it.")
    def execute(self, context):
        if not bpy.data.filepath:  
            bpy.ops.wm.save_as_mainfile('INVOKE_DEFAULT')  
            self.report({'WARNING'}, "N3ST: You must save your .blend file at least once to use this feature.")  
            return {'CANCELLED'}  
        else:
            bpy.ops.wm.save_mainfile()  
        clear_previews()  
        scene = context.scene  
        img = get_image(scene.my_image)  
        if not img:  
            self.report({'WARNING'}, "N3ST: Impossible to load the selected image.")  
            return {'CANCELLED'}
        n_rows = scene.grid_rows  
        n_cols = scene.grid_cols  
        count = n_rows * n_cols  
        scene.color_grid.clear()  
        folder = bpy.path.abspath("//N3ST_grid_palette_icons")  
        for i in range(count):  
            row = i // n_cols  
            col = i % n_cols  
            row_inverted = n_rows - 1 - row  
            color = center_cell_pixel_color(img, row_inverted, col, n_rows, n_cols)  
            item = scene.color_grid.add()  
            item.color = color  
            line = chr(65 + row_inverted)  
            colonne = f"{col + 1:02}"  
            filename = f"col_{line}{colonne}.png"  
            path = create_color_square_image(color, filename, folder)  
            item.icon_path = path  
            make_preview_icon(path)  
        return {'FINISHED'}  
class N3ST_UVEDIT_OP_button_below_picker(bpy.types.Operator):
    bl_idname = "n3st_uvedit.button_below_picker"
    bl_label = "Select the cell"
    index: bpy.props.IntProperty()  
    def execute(self, context):
        scene = context.scene  
        n_rows = scene.grid_rows  
        n_cols = scene.grid_cols  
        index = self.index  
        row = index // n_cols  
        col = index % n_cols  
        row_inverted = n_rows - 1 - row  
        u_min = col / n_cols  
        u_max = (col + 1) / n_cols  
        v_min = row_inverted / n_rows  
        v_max = (row_inverted + 1) / n_rows  
        u_c = (u_min + u_max) / 2  
        v_c = (v_min + v_max) / 2  
        obj = context.active_object  
        if obj is None or obj.type != 'MESH':  
            self.report({'WARNING'}, "N3ST: No active mesh to be found.")
            return {'CANCELLED'}  
        if obj.mode != 'EDIT':  
            self.report({'WARNING'}, "N3ST: You must be in edit mode to use this feature.")  
            return {'CANCELLED'}
        bm = bmesh.from_edit_mesh(obj.data)  
        uv_layer = bm.loops.layers.uv.verify()  
        found = False  
        for face in bm.faces:  
            if face.select:  
                for loop in face.loops:  
                    loop[uv_layer].uv = (u_c, v_c)  
                found = True  
        bmesh.update_edit_mesh(obj.data)  
        if found:
            self.report({'INFO'}, f"N3ST: UVs centered on cell: {chr(65 + row_inverted)}{col + 1:02}")
        else:
            self.report({'WARNING'}, "N3ST: No face(s) selected.")
        return {'FINISHED'}
class N3ST_UVEDIT_OP_open_palette_folder(bpy.types.Operator):
    bl_idname = "n3st_uvedit.open_palette_folder" 
    bl_label = "Open the icons folder"
    bl_description = "Open the folder where the generated images for your icons are saved, within the File Explorer of your system (not in Blender)."
    def execute(self, context):
        import platform  
        folder = bpy.path.abspath("//N3ST_grid_palette_icons")  
        if not os.path.isdir(folder):  
            self.report({'WARNING'}, f"N3ST: couldn't find the folder: {folder}")
            return {'CANCELLED'}
        system = platform.system()  
        import subprocess  
        try:  
            if system == "Windows":  
                os.startfile(folder)  
            elif system == "Darwin":
                subprocess.Popen(["open", folder])  
            else:  
                subprocess.Popen(["xdg-open", folder])  
        except Exception as e:  
            self.report({'ERROR'}, f"N3ST: Impossible to open the folder: {e}")
            return {'CANCELLED'}  
        return {'FINISHED'}  
class N3ST_UVEDIT_OP_clear_color_grid(bpy.types.Operator):
    bl_idname = "n3st_uvedit.clear_color_grid"
    bl_label = "Clear Icons"
    bl_description = ("Remove all the preview icons from your grid. WARNING! It does NOT delete "
                      "the icons from your files. If you wish to delete the generated images, you must do it manually.")  
    def execute(self, context):
        scene = context.scene  
        scene.color_grid.clear()  
        clear_previews()  
        self.report({'INFO'}, "N3ST: Grid icons cleared, showing numbers instead.")
        return {'FINISHED'}
classes = [
    N3ST_UVEDIT_PROP_color_item,
    N3ST_UVEDIT_OP_fill_color_grid,
    N3ST_UVEDIT_OP_button_below_picker,
    N3ST_UVEDIT_OP_open_palette_folder,
    N3ST_UVEDIT_OP_clear_color_grid,
]
def register_properties():
    bpy.types.Scene.my_image = bpy.props.PointerProperty(
        name="Texture", type=bpy.types.Image,
    )
    bpy.types.Scene.grid_rows = bpy.props.IntProperty(name="Rows", default=4, min=1, max=26)
    bpy.types.Scene.grid_cols = bpy.props.IntProperty(name="Columns", default=4, min=1, max=99)
    bpy.types.Scene.color_grid = bpy.props.CollectionProperty(type=N3ST_UVEDIT_PROP_color_item)
def unregister_properties():
    del bpy.types.Scene.my_image
    del bpy.types.Scene.grid_rows
    del bpy.types.Scene.grid_cols
    del bpy.types.Scene.color_grid
    clear_previews()
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    register_properties()
def unregister():
    unregister_properties()
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
