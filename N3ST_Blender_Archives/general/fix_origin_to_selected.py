import bpy
class N3ST_3DVIEW_OT_origintoselect(bpy.types.Operator):
    bl_idname = "n3st_3dview.origintoselect"
    bl_label = "Origin to S."
    bl_description = "Move the origin of the object to the selected vertex, edge or face, in Edit Mode"
    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({'WARNING'}, "N3ST: No object(s) selected.")
            return {'CANCELLED'}
        context.view_layer.objects.active = obj 
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}
classes = [
    N3ST_3DVIEW_OT_origintoselect,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)