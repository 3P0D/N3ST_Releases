import bpy
class N3ST_ANIM_PT_anim_panel_dopesheet(bpy.types.Panel):
    bl_label = "N3ST - Animation"
    bl_idname = "N3ST_ANIM_PT_select_interval_panel"
    bl_space_type = 'DOPESHEET_EDITOR'
    bl_region_type = 'UI'
    bl_category = "N3ST Anim"
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.label(text="FRAME MANAGER:", icon='FORWARD')
        layout.operator("n3st_anim.select_interval_frames")
        layout.separator()
        layout.label(text="BAKE ANIMATION:", icon='FORWARD')
        layout.prop(scene, "bake_action_name", text="Name")
        layout.operator("n3st_anim.anim_from_baked_action", text="Bake New Action")
def register():
    bpy.utils.register_class(N3ST_ANIM_PT_anim_panel_dopesheet)
    bpy.types.Scene.bake_action_name = bpy.props.StringProperty(name="Action", default="")
def unregister():
    del bpy.types.Scene.bake_action_name
    bpy.utils.register_class(N3ST_ANIM_PT_anim_panel_dopesheet)
