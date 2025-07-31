import bpy
import os
from .export_utils import *  
class N3ST_EXPORT_OT_export_fbx(bpy.types.Operator):
    bl_idname = "n3st_export.export_fbx"
    bl_label = "Batch Export FBX"
    bl_description = "Export selection to FBX, following Unity standards."
    def execute(self, context):
        scene = context.scene  
        folder = bpy.path.abspath(scene.n3st_export_folder)  
        object_prefix = scene.n3st_export_object_prefix  
        export_prefix = scene.n3st_export_export_prefix  
        mesh_name = scene.n3st_export_mesh_prefix  
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
            bpy.ops.object.select_all(action='DESELECT')  
            for o in to_export:
                o.select_set(True)  
            bpy.context.view_layer.objects.active = root  
            path = os.path.join(folder, export_name + ".fbx")  
            bpy.ops.export_scene.fbx(
                filepath=path,  
                use_selection=True,  
                apply_unit_scale=True,  
                object_types={'MESH', 'EMPTY', 'ARMATURE', 'OTHER'},  
                mesh_smooth_type='FACE',  
                use_mesh_modifiers=True,  
                add_leaf_bones=False,  
                path_mode='AUTO',  
                bake_space_transform=True,  
                apply_scale_options='FBX_SCALE_UNITS'  
            )
            restore_transforms(saved)  
            restore_mesh_name(obj, mesh_name, object_prefix)  
            total += 1  
        export_message(f"N3ST: {total} objects/hierarchies exported in: {folder}", level="INFO")  
        return {'FINISHED'}  
def register():
    call_for_register()  
    bpy.utils.register_class(N3ST_EXPORT_OT_export_fbx)  
def unregister():
    bpy.utils.unregister_class(N3ST_EXPORT_OT_export_fbx)  
    del bpy.types.Scene.n3st_export_ignore_textures  
    del bpy.types.Scene.n3st_export_with_hierarchy  
    del bpy.types.Scene.n3st_export_reset_transform  
    del bpy.types.Scene.n3st_export_mesh_prefix  
    del bpy.types.Scene.n3st_export_export_prefix  
    del bpy.types.Scene.n3st_export_object_prefix  
    del bpy.types.Scene.n3st_export_folder  
    del bpy.types.Scene.n3st_export_mode 
