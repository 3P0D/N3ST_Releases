import bpy
class N3ST_3DVIEW_OT_clearparents(bpy.types.Operator):
    bl_idname = "n3st_3dview.clearparents"
    bl_label = "Clear parents"
    bl_description = "Break the bonds between the selected objects and their parents, keeping transforms."
    def execute(self, context):
        sel = context.selected_objects
        if not sel:
            self.report({'WARNING'}, "N3ST: No objects selected.")
            return {'CANCELLED'}
        for obj in sel:
            context.view_layer.objects.active = obj
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        return {'FINISHED'}
classes = [
    N3ST_3DVIEW_OT_clearparents,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)