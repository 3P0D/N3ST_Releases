import bpy
class N3ST_3DVIEW_OT_addmodifier_shrinkwrap(bpy.types.Operator):
    bl_idname = "n3st_3dview.addmodifier_shrinkwrap"
    bl_label = "Shrinkwrap (Slct.)"
    bl_description = "Shrinkwrap on ACTIVE object, get the PASSIVE object as target. Adds a Displace modifier."
    def execute(self, context):
        objs = context.selected_objects
        if len(objs) < 2:
            self.report({'WARNING'}, "N3ST: Select at least two objects.")
            return {'CANCELLED'}
        obj = context.active_object
        targets = [o for o in objs if o != obj]
        bpy.ops.object.modifier_add(type='SHRINKWRAP')
        mod = obj.modifiers.get("Shrinkwrap")
        if mod and targets:
            mod.target = targets[0]
        bpy.ops.object.modifier_add(type='DISPLACE')
        disp = obj.modifiers.get("Displace")
        if disp:
            disp.strength = 0.01
            disp.show_on_cage = True
            disp.show_in_editmode = True
        return {'FINISHED'}
classes = [
    N3ST_3DVIEW_OT_addmodifier_shrinkwrap,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)