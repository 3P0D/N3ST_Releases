import bpy
class N3ST_ANIM_OT_select_interval_frames(bpy.types.Operator):
    bl_idname = "n3st_anim.anim_from_baked_action"
    bl_label = "Bake Animation"
    bl_description = "Bake the current action into a new action, taking the first and last frame."
    bl_options = {'REGISTER', 'UNDO'}
    def get_keyframe_range(self, obj):
        if obj.animation_data is None or obj.animation_data.action is None:
            return None, None
        keyframes = []
        for fcurve in obj.animation_data.action.fcurves:
            for kp in fcurve.keyframe_points:
                frame = kp.co.x  
                keyframes.append(frame)  
        if not keyframes:
            return None, None
        return int(min(keyframes)), int(max(keyframes))
    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        if obj is None:
            self.report({'ERROR'}, "N3ST: No active object to be found.")
            return {'CANCELLED'}
        frame_start, frame_end = self.get_keyframe_range(obj)
        if frame_start is None or frame_end is None:
            self.report({'ERROR'}, "N3ST: No keyframes found for active object.")
            return {'CANCELLED'}
        bake_action_name = scene.bake_action_name
        bpy.ops.nla.bake(
            frame_start=frame_start,
            frame_end=frame_end,
            only_selected=False,
            visual_keying=False,
            clear_constraints=False,
            use_current_action=False,
            bake_types={'POSE'}
        )
        if obj.animation_data and obj.animation_data.action:
            obj.animation_data.action.name = bake_action_name
            self.report({'INFO'}, f"N3ST: New action baked under the name: '{bake_action_name}'")
        else:
            self.report({'WARNING'}, "N3ST: No action could be baked.")
        return {'FINISHED'}
classes = [
    N3ST_ANIM_OT_select_interval_frames,
]
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)