import bpy
import bmesh  
class GridUVProperties(bpy.types.PropertyGroup):
    grid_size: bpy.props.IntProperty(
        name="Grid Size",  
        default=8,  
        min=1,  
        max=16,  
    ) 
def ensure_edit_mode(obj):
    if obj and obj.type == "MESH":  
        bpy.context.view_layer.objects.active = obj  
        obj.select_set(True)  
        if bpy.context.mode != 'EDIT_MESH':  
            bpy.ops.object.mode_set(mode='EDIT') 
        return obj  
    return None  
def save_3dview_context(context):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':  
                for space in area.spaces:  
                    if space.type == 'VIEW_3D' and hasattr(space, "region_3d"): 
                        region_3d = space.region_3d  
                        region = next((r for r in area.regions if r.type == 'WINDOW'), None)  
                        return {  
                            'window': window,
                            'area': area,
                            'region': region,
                            'rot': region_3d.view_rotation.copy(),  
                            'loc': region_3d.view_location.copy(),  
                            'persp': region_3d.view_perspective,  
                            'dist': getattr(region_3d, "view_distance", None),  
                        }
    return None  
def restore_3dview_context(viewContext):
    if not viewContext:  
        return
    area = viewContext['area']  
    for space in area.spaces:  
        if space.type == 'VIEW_3D' and hasattr(space, "region_3d"):  
            region_3d = space.region_3d  
            region_3d.view_rotation = viewContext['rot']  
            region_3d.view_location = viewContext['loc']  
            region_3d.view_perspective = viewContext['persp']  
            if viewContext['dist'] is not None:  
                region_3d.view_distance = viewContext['dist']  
            break  
def set_view_axis(context, viewContext, axis_key):
    axis_map = {'X': 'RIGHT', 'Y': 'FRONT', 'Z': 'TOP'}  
    axis_type = axis_map.get(axis_key, 'TOP')  
    if viewContext and viewContext['window'] and viewContext['area'] and viewContext['region']:  
        with bpy.context.temp_override(window=viewContext['window'], area=viewContext['area'], region=viewContext['region']):  
            bpy.ops.view3d.view_axis(type=axis_type, align_active=False)  
            bpy.ops.view3d.view_persportho()  
            bpy.ops.view3d.view_selected()  
def project_from_view(obj, report):
    if not obj.data.uv_layers.active:  
        report({'WARNING'}, "N3ST: No active UVMap found.") 
        return False
    try:
        bpy.ops.uv.project_from_view(orthographic=True, scale_to_bounds=True)  
    except RuntimeError:  
        report({'ERROR'}, "N3ST: Project from view impossible.")
        return False  
    return True  
def stretch_uv_to_cell(obj, cell, grid_size, axis, report):
    bm = bmesh.from_edit_mesh(obj.data)  
    uv_layer = bm.loops.layers.uv.active  
    selected_uvs = [l[uv_layer].uv for f in bm.faces if f.select for l in f.loops]  
    if not selected_uvs:  
        report({'WARNING'}, "N3ST: There is no selected face(s).")
        return False
    u0 = min(uv[0] for uv in selected_uvs)  
    u1 = max(uv[0] for uv in selected_uvs)  
    v0 = min(uv[1] for uv in selected_uvs)  
    v1 = max(uv[1] for uv in selected_uvs)  
    du = (u1 - u0) or 1.0  
    dv = (v1 - v0) or 1.0  
    step = 1.0 / grid_size  
    if cell < 0 or cell >= grid_size:  
        report({'WARNING'}, f"N3ST: Cell {cell} out of grid range 0-{grid_size-1}.")  
        return False  
    u_min = cell * step  
    for uv in selected_uvs:
        uv[0] = ((uv[0] - u0) / du) * step + u_min  
        uv[1] = (uv[1] - v0) / dv  
    median_u = sum(uv[0] for uv in selected_uvs) / len(selected_uvs)  
    median_v = sum(uv[1] for uv in selected_uvs) / len(selected_uvs)  
    for uv in selected_uvs:
        uv[0] = median_u + (uv[0] - median_u) * 0.5  
        uv[1] = median_v + (uv[1] - median_v) * 0.99  
    bmesh.update_edit_mesh(obj.data)  
    report({'INFO'}, f"N3ST: UV projected on cell {axis}{cell+1}.")  
    return True  
def project_and_stretch(context, obj, cell, grid_size, axis, report):
    if not project_from_view(obj, report):  
        return False  
    return stretch_uv_to_cell(obj, cell, grid_size, axis, report)  
class N3ST_UVEDIT_OT_project_gradient_uv(bpy.types.Operator):
    bl_idname = "n3st_uv.grid_button_gradient_uv_projection"
    bl_label = "UV Project from axis cell (X/Y/Z), stretching it within the Y of the cell."
    bl_options = {'REGISTER', 'UNDO'}
    axis: bpy.props.EnumProperty(  
        items=[
            ('X', "RIGHT", "Right (X)"),  
            ('Y', "FRONT", "Front (Y)"),  
            ('Z', "TOP", "Top (Z)"),  
        ],
        name="Axe"  
    ) 
    cell: bpy.props.IntProperty() 
    _viewContext = None  
    _timer = None  
    _phase = 0  
    _object_name = None  
    def invoke(self, context, event):
        obj = ensure_edit_mode(context.active_object)  
        if obj is None:  
            self.report({'WARNING'}, "N3ST: Select an object in Edit Mode.")  
            return {'CANCELLED'}  
        self._object_name = obj.name  
        self._viewContext = save_3dview_context(context)  
        if not self._viewContext or not self._viewContext['region']:  
            self.report({'WARNING'}, "N3ST: Impossible to access to an active 3D View.")  
            return {'CANCELLED'}
        if self.cell < 0:  
            self.report({'WARNING'}, "N3ST: Cell must be non-negative.")
            return {'CANCELLED'}
        grid_props = getattr(context.scene, "grid_uv_props", None)  
        if not grid_props or not hasattr(grid_props, "grid_size"):  
            self.report({'WARNING'}, "N3ST: grid_uv_props.grid_size not found in scene.")  
            return {'CANCELLED'}
        set_view_axis(context, self._viewContext, self.axis)  
        self._phase = 0  
        wm = context.window_manager  
        self._timer = wm.event_timer_add(0.1, window=context.window)  
        wm.modal_handler_add(self)  
        return {'RUNNING_MODAL'}  
    def modal(self, context, event):
        if event.type != 'TIMER':  
            return {'PASS_THROUGH'}  
        if self._phase == 0:  
            self._phase = 1  
            obj = bpy.data.objects.get(self._object_name)  
            ok = project_and_stretch(context, obj, self.cell, context.scene.grid_uv_props.grid_size, self.axis, self.report)  
            restore_3dview_context(self._viewContext)  
            context.window_manager.event_timer_remove(self._timer)  
            return {'FINISHED' if ok else 'CANCELLED'}  
        return {'PASS_THROUGH'}  
classes = [GridUVProperties, N3ST_UVEDIT_OT_project_gradient_uv]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.grid_uv_props = bpy.props.PointerProperty(type=GridUVProperties)  
def unregister():
    del bpy.types.Scene.grid_uv_props
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
