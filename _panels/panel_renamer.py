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
        items = [
            ("n3st_renamer.applyname_geo", "GEO"),
            ("n3st_renamer.applyname_rig", "RIG"),
            ("n3st_renamer.applyname_empty", "EMPTY"),
            ("n3st_renamer.applyname_curve", "CURVE"),
            ("n3st_renamer.applyname_bool", "BOOL"),
        ]
        for op_idname, label_text in items:
            row = layout.row(align=True)
            split = row.split(factor=0.7)
            col_left = split.column()
            col_right = split.column()
            op = col_right.operator(op_idname, text=label_text)
            col_left.prop(op, "prefix")
def register():
    bpy.utils.register_class(N3ST_PT_rename_panel)
def unregister():
    bpy.utils.unregister_class(N3ST_PT_rename_panel)
