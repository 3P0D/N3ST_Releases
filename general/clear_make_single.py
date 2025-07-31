import bpy
class N3ST_3DVIEW_OT_makesingle(bpy.types.Operator):
    bl_idname = "n3st_3dview.makesingle"
    bl_label = "Make single"
    bl_description = "Break the bonds between the selected objects and their datas, making them all unique users"
    def execute(self, context):
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, animation=False, obdata_animation=False)
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_makesingle)
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_makesingle)
