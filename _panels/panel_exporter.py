import bpy
class N3ST_PT_export_panel(bpy.types.Panel):
    bl_label = "N3ST - Exporter"
    bl_idname = "N3ST_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "N3ST Objects"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="Batch export your selected objects.")
        layout.separator()
        layout.prop(scene, "n3st_export_mode") 
        layout.prop(scene, "n3st_export_folder")
        layout.separator()
        layout.label(text="SET PREFIXES:", icon='MENU_PANEL')
        layout.prop(scene, "n3st_export_object_prefix")
        layout.prop(scene, "n3st_export_export_prefix")
        layout.prop(scene, "n3st_export_mesh_prefix", text="Mesh")
        layout.separator()
        layout.prop(scene, "n3st_export_reset_transform")
        layout.prop(scene, "n3st_export_with_hierarchy")
        if scene.n3st_export_mode == 'GLBGLTF':
            layout.prop(scene, "n3st_export_ignore_textures", text="Remove Textures from Export")
            layout.separator()
            layout.operator("n3st_export.export_glb", text="Export GLB")
            layout.operator("n3st_export.export_gltf", text="Export GLTF (+bin+tex)")
        elif scene.n3st_export_mode == 'FBX':
            layout.separator()
            layout.operator("n3st_export.export_fbx", text="Export FBX")
def register():
    bpy.utils.register_class(N3ST_PT_export_panel)
def unregister():
    bpy.utils.unregister_class(N3ST_PT_export_panel)
