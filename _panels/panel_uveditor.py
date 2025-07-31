import bpy
import os
MAX_GRID_SIZE = 16
class N3ST_UVEDIT_PT_Gradient_Flat_Projection_3DView(bpy.types.Panel):
    bl_label = "N3ST - UVs EDIT"
    bl_idname = "N3ST_PT_uv_grid_panel_3d"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "N3ST UVs"
    def draw(self, context):
        layout = self.layout
        layout.label(text="UV PROJECTION:", icon='FORWARD')
        layout.prop(context.scene, "n3st_uv_mode", expand=True)
        layout.separator()
        if context.scene.n3st_uv_mode == 'FLAT':
            scene = context.scene
            layout.template_ID(scene, "my_image", new="image.new", open="image.open")
            row = layout.row(align=True)
            row.prop(scene, "grid_rows")
            row.prop(scene, "grid_cols")
            row = layout.row(align=True)
            row.operator("n3st_uvedit.clear_color_grid", text="Clear Preview")
            row.operator("n3st_uvedit.fill_color_grid", text="Generate Icons")
            row.operator("n3st_uvedit.open_palette_folder", text="", icon="FILE_FOLDER")
            layout.separator()
            grid = layout.grid_flow(
                columns=scene.grid_cols,
                even_columns=True,
                even_rows=True,
                align=True,
                row_major=True
            )
            count = scene.grid_rows * scene.grid_cols
            try:
                from .uveditor.grid_projection_uv_flat import preview_col
            except ImportError:
                preview_col = None
            for i in range(count):
                col_layout = grid.column(align=True)
                row_num = i // scene.grid_cols
                col_num = i % scene.grid_cols
                lettre_col = chr(65 + col_num)
                numbers_row = (row_num % 8) + 1
                if i < len(scene.color_grid):
                    item = scene.color_grid[i]
                    path = item.icon_path
                    icon_name = os.path.basename(path)
                    if preview_col and icon_name in preview_col:
                        icon_id = preview_col[icon_name].icon_id
                    else:
                        icon_id = 0
                    btn_col = col_layout.column()
                    btn_col.scale_x = 1.0
                    btn_col.scale_y = 1.0
                    if icon_id != 0:
                        op = btn_col.operator("n3st_uvedit.button_below_picker", text="", icon_value=icon_id)
                    else:
                        display = f"{lettre_col}{numbers_row}"
                        op = btn_col.operator("n3st_uvedit.button_below_picker", text=display, icon_value=0)
                    op.index = i
                else:
                    display = f"{lettre_col}{numbers_row}"
                    op = col_layout.operator("n3st_uvedit.button_below_picker", text=display, icon_value=0)
                    op.index = i
        elif context.scene.n3st_uv_mode == 'GRADIENT':
            props = getattr(context.scene, "grid_uv_props", None)
            if not props:
                layout.label(text="N3ST: grid_uv_props property missing", icon='ERROR')
                return
            grid_size = props.grid_size
            if grid_size > MAX_GRID_SIZE:
                layout.label(text=f"N3ST: Maximum grid size: {MAX_GRID_SIZE}", icon='ERROR')
                grid_size = MAX_GRID_SIZE
            layout.prop(props, "grid_size")
            layout.separator()
            for axis in ['X', 'Y', 'Z']:
                row = layout.row(align=True)
                row.label(text=axis)
                for cell in range(grid_size):
                    op = row.operator("n3st_uv.grid_button_gradient_uv_projection", text=f"{cell+1}")
                    op.axis = axis
                    op.cell = cell
classes = [N3ST_UVEDIT_PT_Gradient_Flat_Projection_3DView]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    if not hasattr(bpy.types.Scene, "n3st_uv_mode"):
        bpy.types.Scene.n3st_uv_mode = bpy.props.EnumProperty(
            name="Mode UV",
            items=[('FLAT', "Flat", "UV point in cell"),
                   ('GRADIENT', "Gradient", "UV gradient per cell")],
            default='FLAT',
        )
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    if hasattr(bpy.types.Scene, "n3st_uv_mode"):
        del bpy.types.Scene.n3st_uv_mode
