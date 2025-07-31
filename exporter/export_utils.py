import bpy
import os
def export_message(message, level="INFO"):
    wm = bpy.context.window_manager  
    wm.popup_menu(lambda self, context: self.layout.label(text=message), title=level.capitalize())  
    print(f"[N3ST_EXPORT][{level}] {message}")  
def create_folder_if_needed(folder):
    os.makedirs(folder, exist_ok=True)  
def rename_object_for_export(name, object_prefix, export_prefix):
    if object_prefix:
        return name.replace(object_prefix, export_prefix, 1)  
    return name  
def set_mesh_name(obj, mesh_name):
    original_name = obj.data.name  
    if mesh_name.strip():
        obj.data.name = mesh_name.strip()  
    return original_name  
def restore_mesh_name(obj, mesh_name, object_prefix):
    prefix = mesh_name.strip()  
    objname_clean = obj.name  
    if object_prefix and objname_clean.startswith(object_prefix):
        objname_clean = objname_clean[len(object_prefix):]  
    obj.data.name = prefix + objname_clean  
def disconnect_img_textures(obj):
    cache = {}  
    for slot in obj.material_slots:  
        mat = slot.material  
        if mat and mat.use_nodes:  
            tree = mat.node_tree  
            removed = []  
            for node in tree.nodes:
                if node.type == 'TEX_IMAGE':  
                    for out_idx, out in enumerate(node.outputs):
                        for link in list(out.links):  
                            removed.append((node.name, out_idx, link.to_node.name, list(link.to_node.inputs).index(link.to_socket)))
                            tree.links.remove(link)  
            cache[mat.name] = removed  
    return cache  
def reconnect_img_textures(obj, cache):
    for slot in obj.material_slots:
        mat = slot.material
        if mat and mat.use_nodes and mat.name in cache:  
            tree = mat.node_tree
            for from_node, from_idx, to_node, to_idx in cache[mat.name]:
                f_node = tree.nodes.get(from_node)  
                t_node = tree.nodes.get(to_node)    
                if f_node and t_node:
                    tree.links.new(list(f_node.outputs)[from_idx], list(t_node.inputs)[to_idx])
def collect_hierarchy(obj):
    objs = {obj}  
    def add_children(o):
        for child in o.children:
            objs.add(child)  
            add_children(child)  
    add_children(obj)  
    return objs  
def find_armature_or_empty_parent(obj):
    cur = obj
    root = None
    while cur.parent:
        if cur.parent.type in {'ARMATURE', 'EMPTY'}:
            root = cur.parent  
        cur = cur.parent
    return root  
def reset_transforms(parent, objs, with_hierarchy, do_reset):
    backup = {}  
    if do_reset:
        if with_hierarchy:
            backup[parent] = (
                parent.location.copy(),
                parent.rotation_euler.copy(),
                parent.scale.copy()
            )
            parent.location = (0, 0, 0)
            parent.rotation_euler = (0, 0, 0)
            parent.scale = (1, 1, 1)
        else:
            for o in objs:
                backup[o] = (
                    o.location.copy(),
                    o.rotation_euler.copy(),
                    o.scale.copy()
                )
                o.location = (0, 0, 0)
                o.rotation_euler = (0, 0, 0)
                o.scale = (1, 1, 1)
    return backup  
def restore_transforms(backup):
    for o, (loc, rot, scale) in backup.items():
        o.location = loc
        o.rotation_euler = rot
        o.scale = scale
def call_for_register():
    bpy.types.Scene.n3st_export_mode = bpy.props.EnumProperty(
        name="Format",
        items=[
            ("GLBGLTF", "GLB/GLTF", "Export in GLB or GLTF"),  
            ("FBX", "FBX", "Export in FBX"),
        ],
        default="GLBGLTF"
    )
    bpy.types.Scene.n3st_export_folder = bpy.props.StringProperty(
        name="Folder",
        subtype='DIR_PATH',
        default="//",
        description="Path to export to. Best practice is to export directly into the project."
    )
    bpy.types.Scene.n3st_export_object_prefix = bpy.props.StringProperty(
        name="Object",
        default="GEO",
        description="Prefix of the object in the Blender file. Reference to rename the file with proper prefix."
    )
    bpy.types.Scene.n3st_export_export_prefix = bpy.props.StringProperty(
        name="Export",
        default="3d",
        description="Prefix to replace as export."
    )
    bpy.types.Scene.n3st_export_mesh_prefix = bpy.props.StringProperty(
        name="Datas",
        default="MESH",
        description="Rename the Mesh Datas of the object for export. Mostly for Godot."
    )
    bpy.types.Scene.n3st_export_reset_transform = bpy.props.BoolProperty(
        name="Reset Transform",
        default=True,
        description="Reset the transform to 0-0-1. If not active, will export as is."
    )
    bpy.types.Scene.n3st_export_with_hierarchy = bpy.props.BoolProperty(
        name="Preserve Hierarchy",
        default=True,
        description="Export the children of the parent within the same file. If not active, export separately."
    )
    bpy.types.Scene.n3st_export_ignore_textures = bpy.props.BoolProperty(
        name="Ignore Textures",
        default=False,
        description="Remove the textures while exporting to avoid multiple texture within the export folder."
    )
