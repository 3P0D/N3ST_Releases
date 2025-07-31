import bpy
class N3ST_RENAMER_OT_applyname_curve(bpy.types.Operator):
    bl_idname = "n3st_renamer.applyname_curve"
    bl_label = "Curve"
    bl_description = "Rename the selection of CURVES into a given prefix."
    bl_options = {'REGISTER', 'UNDO'}
    def execute(self, context):
        sel = context.selected_objects
        prefix = getattr(context.scene, 'newName_curve', "")
        any_renamed = False
        for obj in sel:
            if obj.type == 'CURVE':
                if not obj.name.startswith(prefix):
                    obj.name = prefix + "_" + obj.name
                    any_renamed = True
        return {'FINISHED'} if any_renamed else {'CANCELLED'}
def register():
    bpy.types.Scene.newName_curve = bpy.props.StringProperty(name="Curve", default="CURV")
    bpy.utils.register_class(N3ST_RENAMER_OT_applyname_curve)
def unregister():
    bpy.utils.unregister_class(N3ST_RENAMER_OT_applyname_curve)
    del bpy.types.Scene.newName_curve
