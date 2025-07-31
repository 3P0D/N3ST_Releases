import bpy
class N3ST_3DVIEW_OT_createsuzanne(bpy.types.Operator):
    bl_idname = "n3st_3dview.createsuzanne"
    bl_label = "Suzanne (0,0,0)"
    bl_description = "Create a SUZANNE object at location 0,0,0"
    def execute(self, context):
        bpy.ops.mesh.primitive_monkey_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        obj = context.active_object
        if obj:
            obj.name = "_SUZANNE"
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_createsuzanne)
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_createsuzanne)
