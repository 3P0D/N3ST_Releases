import bpy
import os
from .export_utils import *  
class N3ST_EXPORT_OT_export_glb(bpy.types.Operator):
    bl_idname = "n3st_export.export_glb"
    bl_label = "Batch Export GLB"
    bl_description = "Export selection to GLB binary (ready for Godot)."
    def execute(self, context):
        scene = context.scene  
        folder = bpy.path.abspath(scene.n3st_export_folder)  
        object_prefix = scene.n3st_export_object_prefix  
        export_prefix = scene.n3st_export_export_prefix  
        mesh_name = scene.n3st_export_mesh_prefix  
        ignore_textures = getattr(scene, "n3st_export_ignore_textures", False)
        reset = scene.n3st_export_reset_transform  
        hierarchy = scene.n3st_export_with_hierarchy  
        try:
            create_folder_if_needed(folder)  
        except Exception as e:
            export_message(f"N3ST: Failure at folder creation: {e}", level="ERROR")  
            return {'CANCELLED'}  
        total = 0  
        exported = set()  
        for obj in context.selected_objects:  
            if obj.type != 'MESH' or obj in exported:
                continue  
            if hierarchy:
                parent_root = find_armature_or_empty_parent(obj)  
                if parent_root:
                    root = parent_root  
                else:
                    root = obj  
                to_export = collect_hierarchy(root)  
            else:
                root = obj  
                to_export = {obj}  
            if any(o in exported for o in to_export):
                continue  
            exported.update(to_export)  
            export_name = rename_object_for_export(root.name, object_prefix, export_prefix)  
            original_name = set_mesh_name(obj, mesh_name)  
            saved = reset_transforms(root, to_export, hierarchy, reset)  
            tex_cache = {}  
            if ignore_textures:  
                for o in to_export:
                    if o.type == 'MESH':
                        tex_cache[o.name] = disconnect_img_textures(o)  
            bpy.ops.object.select_all(action='DESELECT')  
            for o in to_export:
                o.select_set(True)  
            bpy.context.view_layer.objects.active = root  
            path = os.path.join(folder, export_name + ".glb")  
            bpy.ops.export_scene.gltf(
                filepath=path,  
                export_format='GLB',  
                use_selection=True,  
                export_apply=True,  
                export_materials='EXPORT',  
                export_normals=True,  
            )
            if ignore_textures:  
                for o in to_export:
                    if o.type == 'MESH' and o.name in tex_cache:
                        reconnect_img_textures(o, tex_cache[o.name])  
            restore_transforms(saved)  
            restore_mesh_name(obj, mesh_name, object_prefix)  
            total += 1  
        export_message(f"N3ST: {total} objects/hierarchies exported in: {folder}", level="INFO")  
        return {'FINISHED'}
def register():
    call_for_register()
    bpy.utils.register_class(N3ST_EXPORT_OT_export_glb)
def unregister():
    bpy.utils.unregister_class(N3ST_EXPORT_OT_export_glb)
    del bpy.types.Scene.n3st_export_ignore_textures
    del bpy.types.Scene.n3st_export_with_hierarchy
    del bpy.types.Scene.n3st_export_reset_transform
    del bpy.types.Scene.n3st_export_mesh_prefix
    del bpy.types.Scene.n3st_export_export_prefix
    del bpy.types.Scene.n3st_export_object_prefix
    del bpy.types.Scene.n3st_export_folder
