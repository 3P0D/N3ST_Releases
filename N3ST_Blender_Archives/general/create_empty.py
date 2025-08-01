import bpy
class N3ST_3DVIEW_OT_createempty(bpy.types.Operator):
    bl_idname = "n3st_3dview.createempty"
    bl_label = "Empty (0,0,0)"
    bl_description = "Create an EMPTY object at location 0,0,0"
    def execute(self, context):
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        obj = context.active_object
        if obj:
            obj.name = "_EMPTY"
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_createempty)
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_createempty)
