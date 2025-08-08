import bpy
class N3ST_3DVIEW_OT_applyrotation_rig(bpy.types.Operator):
    bl_idname = "n3st_3dview.applyrotation_rig"
    bl_label = "Apply -90 (Rig)"
    bl_description = "Apply a -90° rotation on a rig to prepare it for export in Unity"
    def execute(self, context):
        obj = context.object
        if obj is None or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "N3ST: Select an Armature object.")
            return {'CANCELLED'}
        context.view_layer.objects.active = obj
        if round(obj.rotation_euler.x, 5) != -1.5708:
            obj.rotation_euler = (0.0, 0.0, 0.0)
            obj.rotation_euler.x = 1.5708
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            obj.rotation_euler.x = -1.5708
        return {'FINISHED'}
classes = [
    N3ST_3DVIEW_OT_applyrotation_rig,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)