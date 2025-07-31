import bpy
class N3ST_3DVIEW_OT_applytransform(bpy.types.Operator):
    bl_idname = "n3st_3dview.applytransform"
    bl_label = "Apply all"
    bl_description = "Apply all the transform of an object: location, rotation, scale"
    def execute(self, context):
        obj = context.object
        if obj is None:
            self.report({'WARNING'}, "N3ST: No object(s) selected.")
            return {'CANCELLED'}
        context.view_layer.objects.active = obj
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_applytransform)
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_applytransform)
