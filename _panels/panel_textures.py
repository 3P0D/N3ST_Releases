import bpy
from ..textures import add_debug_material 
COLS_PER_ROW = 8  
class N3ST_PT_texture_panel(bpy.types.Panel):
    bl_label = "N3ST - Materials/Textures"
    bl_idname = "n3st_texmat_PT_panelC"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "N3ST Core"
    def draw(self, context):
        layout = self.layout  
        scene = context.scene  
        if not hasattr(scene, "color_count") or not hasattr(scene, "my_colors"):
            layout.label(text="No palette initiated.")  
            return  
        layout.label(text="Manage your debug textures and materials.")
        layout.separator()  
        layout.label(text="ADD CHECKER TEXTURES:", icon='FORWARD')
        row = layout.row()
        row.operator("n3st_texmat.addchecker_512", text="512")  
        row.operator("n3st_texmat.addchecker_1024", text="1024")  
        row.operator("n3st_texmat.addchecker_2048", text="2048")  
        row.operator("n3st_texmat.addchecker_4096", text="4096")  
        layout.separator()  
        layout.label(text="ADD DEBUG MATERIALS:", icon='FORWARD')
        row = layout.row()
        row.prop(scene, "color_count", text="Colours:")  
        row.operator("n3st_texmat.pick_debug_palette", text="", icon="SEQ_SEQUENCER")  
        items = scene.my_colors  
        n = scene.color_count  
        if not items:
            layout.label(text="No color picker initiated.")
            return 
        for rowi in range((n + COLS_PER_ROW - 1) // COLS_PER_ROW):
            row = layout.row(align=True)  
            for coli in range(COLS_PER_ROW):
                idx = rowi * COLS_PER_ROW + coli  
                if idx < n:  
                    box = row.column(align=True)  
                    ccol = box.column(align=True)  
                    ccol.scale_y = 1  
                    ccol.prop(items[idx], "color", text="")  
                    cbtn = box.column(align=True)  
                    cbtn.scale_y = 0.5  
                    op = cbtn.operator("n3st_texmat.pick_assign_mat", text="", icon='DOT')  
                    op.idx = idx  
def register():
    bpy.utils.register_class(N3ST_PT_texture_panel)
def unregister():
    bpy.utils.unregister_class(N3ST_PT_texture_panel)
