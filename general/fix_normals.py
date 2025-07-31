import bpy
class N3ST_3DVIEW_OT_fixnormals(bpy.types.Operator):
    bl_idname = "n3st_3dview.fixnormals"
    bl_label = "Fix normals"
    bl_description = "Fix the inverted normals of all selected mesh objects instantly, in Object Mode"
    def execute(self, context):
        sel = context.selected_objects
        if not sel:
            self.report({'WARNING'}, "N3ST: No objects selected.")
            return {'CANCELLED'}
        for obj in sel:
            if obj.type != "MESH":
                continue
            context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.normals_make_consistent(inside=False)
            bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_fixnormals)
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_fixnormals)
