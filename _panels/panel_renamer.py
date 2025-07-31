import bpy
class N3ST_PT_rename_panel(bpy.types.Panel):
    bl_label = "N3ST - Renamer"
    bl_idname = "N3ST_RENAMER_PT_naming_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "N3ST Objects" 
    def draw(self, context):
        layout = self.layout
        layout.label(text="Fast renaming options for your objects.")
        layout.separator()
        layout.label(text="SET PREFIXES:", icon='MENU_PANEL')
        split = layout.split(factor=0.66)
        split.prop(context.scene, 'newName_geo')
        split.operator("n3st_renamer.applyname_geo")
        split = layout.split(factor=0.66)
        split.prop(context.scene, 'newName_rig')
        split.operator("n3st_renamer.applyname_rig")
        split = layout.split(factor=0.66)
        split.prop(context.scene, 'newName_empty')
        split.operator("n3st_renamer.applyname_empty")
        split = layout.split(factor=0.66)
        split.prop(context.scene, 'newName_curve')
        split.operator("n3st_renamer.applyname_curve")
        split = layout.split(factor=0.66)
        split.prop(context.scene, 'newName_bool')
        split.operator("n3st_renamer.applyname_bool")
def register():
    bpy.utils.register_class(N3ST_PT_rename_panel)
def unregister():
    bpy.utils.unregister_class(N3ST_PT_rename_panel)
