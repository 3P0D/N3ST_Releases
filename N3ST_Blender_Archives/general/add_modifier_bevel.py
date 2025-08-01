import bpy
class N3ST_3DVIEW_OT_addmodifier_bevel(bpy.types.Operator):
    bl_idname = "n3st_3dview.addmodifier_bevel"
    bl_label = "Bevel (Weight)"
    bl_description = "Add a BEVEL modifier with the WEIGHT option toggled on."
    def execute(self, context):
        obj = context.object  
        if obj is None or (not hasattr(obj, "modifiers")):  
            self.report({'WARNING'}, "N3ST: No object(s) selected.")  
            return {'CANCELLED'}  
        bpy.ops.object.modifier_add(type='BEVEL')  
        mod = obj.modifiers.get("Bevel")  
        if mod:
            mod.limit_method = 'WEIGHT'  
        return {'FINISHED'}  
def register():
    bpy.utils.register_class(N3ST_3DVIEW_OT_addmodifier_bevel)  
def unregister():
    bpy.utils.unregister_class(N3ST_3DVIEW_OT_addmodifier_bevel)
