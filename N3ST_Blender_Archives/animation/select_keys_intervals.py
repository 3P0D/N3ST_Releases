import bpy
class N3ST_ANIM_OT_select_interval_frames(bpy.types.Operator):
    bl_idname = "n3st_anim.select_interval_frames"
    bl_label = "Select Frame Intervals"
    bl_description = "Select all keyframes from a given range intervals (+ the first and last frame)."
    bl_options = {'REGISTER', 'UNDO'}
    interval: bpy.props.IntProperty(
        name="Interval (frames)",
        description="Select a keyframe every X frames.",
        default=10,
        min=1
    )  
    def execute(self, context):
        action = context.object.animation_data.action if context.object and context.object.animation_data else None
        if not action:
            self.report({'WARNING'}, "N3ST: No action/keys found within the selected object.")
            return {'CANCELLED'}
        bpy.ops.action.select_all(action='DESELECT')
        start_frame = int(action.frame_range[0])
        end_frame = int(action.frame_range[1])
        for fcurve in action.fcurves:
            for i, keyframe in enumerate(fcurve.keyframe_points):
                frame = int(keyframe.co.x)
                keyframe.select_control_point = (frame == start_frame) or (frame == end_frame) or (frame % self.interval == 0)
        context.area.tag_redraw()
        self.report({'INFO'}, f"N3ST: Keyframe(s) selected at {self.interval} intervals.")
        return {'FINISHED'}
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
classes = [
    N3ST_ANIM_OT_select_interval_frames,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
