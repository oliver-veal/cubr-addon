import bpy


class OperatorView(bpy.types.Operator):
    """Toggle show render view"""
    bl_idname = "cubr.view_show"
    bl_label = "View Render"

    def execute(self, context):
        bpy.ops.render.view_show('INVOKE_DEFAULT')

        img = None
        for image in bpy.data.images:
            if image.name == "Cubr Render Result.png":
                img = image
                break

        if img is not None:
            for screen in bpy.data.screens:
                for area in screen.areas:
                    if area.type == 'IMAGE_EDITOR':
                        area.spaces.active.image = img
                        area.tag_redraw()

        return {'FINISHED'}
