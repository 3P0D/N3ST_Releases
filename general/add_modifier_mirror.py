import bpy
class N3ST_3DVIEW_OT_addmodifier_mirror(bpy.types.Operator):
    bl_idname = "n3st_3dview.addmodifier_mirror"
    bl_label = "Mirror (X)"
    bl_description = "Add a MIRROR modifier on the X axis, with clipping toggled on"
    def execute(self, context):
        if context.object is None or not hasattr(context.object, "modifiers"):
            self.report({'WARNING'}, "N3ST: No object(s) selected.")
            return {'CANCELLED'}
        obj = context.object
        bpy.ops.object.modifier_add(type='MIRROR')
        mod = obj.modifiers.get("Mirror")
        if mod:
            mod.use_clip = True
            mod.show_on_cage = True
            mod.show_in_editmode = True
        return {'FINISHED'}
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_addmodifier_mirror)
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_addmodifier_mirror)
