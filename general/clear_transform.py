import bpy
class N3ST_3DVIEW_OT_cleartransform(bpy.types.Operator):
    bl_idname = "n3st_3dview.cleartransform"
    bl_label = "Clear all"
    bl_description = "Clear all the transform of the selected objects: location, rotation, scale."
    def execute(self, context):
        sel = context.selected_objects
        if not sel:
            self.report({'WARNING'}, "N3ST: No objects selected.")
            return {'CANCELLED'}
        for obj in sel:
            context.view_layer.objects.active = obj
            bpy.ops.object.location_clear(clear_delta=False)
            bpy.ops.object.rotation_clear(clear_delta=False)
            bpy.ops.object.scale_clear(clear_delta=False)
        return {'FINISHED'}
classes = [
    N3ST_3DVIEW_OT_cleartransform,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)