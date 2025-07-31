import bpy
class N3ST_PT_main_panel(bpy.types.Panel):
    bl_label = "N3ST - Core"
    bl_idname = "N3ST_3DVIEW_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "N3ST Core"
    def draw(self, context):
        self.layout.label(text="Because I'm lazy. Distributed as is.")
        layout = self.layout
        layout.separator()
        layout.label(text="TRANSFORMS:", icon='FORWARD')
        row = layout.row()
        row.operator("n3st_3dview.applytransform", icon='CURVE_NCIRCLE')
        row.operator("n3st_3dview.cleartransform", icon='TRASH')
        layout.operator("n3st_3dview.applyrotation_rig", icon='TRACKING_REFINE_FORWARDS')
        layout.separator()
        layout.label(text="GEOMETRY:", icon='FORWARD')
        row = layout.row()
        row.operator("n3st_3dview.fixnormals", icon='ORIENTATION_NORMAL')
        row.operator("n3st_3dview.origintoselect", icon='PIVOT_CURSOR')
        layout.separator()
        layout.label(text="PARENTS:", icon='FORWARD')
        row = layout.row()
        row.operator("n3st_3dview.makesingle", icon='ORPHAN_DATA')
        row.operator("n3st_3dview.clearparents", icon='GHOST_DISABLED')
        layout = self.layout
        layout.separator()
        layout.label(text="ADD OBJECTS:", icon='FORWARD')
        row = layout.row()
        row.operator("n3st_3dview.createempty", icon='EMPTY_AXIS')
        row.operator("n3st_3dview.createsuzanne", icon='MONKEY')
        layout.separator()
        layout.label(text="ADD MODIFIERS:", icon='FORWARD')
        row = layout.row()
        row.operator("n3st_3dview.addmodifier_mirror", icon='MOD_MIRROR')
        row.operator("n3st_3dview.addmodifier_bevel", icon='MOD_BEVEL')
        layout.operator("n3st_3dview.addmodifier_shrinkwrap", icon='MOD_SHRINKWRAP')
        row = layout.row()
        row.prop(context.scene, 'n3st_prepare_sculpt_remesh', text="Remesh Size")
        row.operator("n3st_3dview.prepsculpt", icon='SCULPTMODE_HLT')
def register():
        bpy.utils.register_class(N3ST_PT_main_panel)
def unregister():
        bpy.utils.unregister_class(N3ST_PT_main_panel)
