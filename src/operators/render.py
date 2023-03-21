from bpy.types import Operator
import bpy

import os

from .. import props
from ..timers.render import poll_render


class OperatorRenderImage(Operator):
    bl_label = "Render Image"
    bl_idname = "cubr.render_image"

    enabled_description = "Render a still from the active scene with Cubr"
    disabled_description = """Render a still from the active scene with Cubr.

Cubr is disabled because you have not saved your file yet.
Save the file to enable rendering"""

    @classmethod
    def description(self, context, properties) -> str:
        enabled = props.is_addon_enabled and props.is_file_ready
        return self.enabled_description if enabled else self.disabled_description

    def execute(self, context):
        return execute(self, context, False)


class OperatorRenderAnimation(Operator):
    bl_label = "Render Animation"
    bl_idname = "cubr.render_animation"

    enabled_description = "Render an animation from the active scene with Cubr"
    disabled_description = """Render an animation from the active scene with Cubr.

Cubr is disabled because you have not saved your file yet.
Save the file to enable rendering"""

    @classmethod
    def description(self, context, properties) -> str:
        enabled = props.is_addon_enabled and props.is_file_ready
        return self.enabled_description if enabled else self.disabled_description

    def execute(self, context):
        return execute(self, context, True)


class OperatorCancelRender(Operator):
    """Cancel the current render."""
    bl_label = "Cancel Render"
    bl_idname = "cubr.cancel_render"

    def execute(self, context):
        if not props.is_addon_enabled:
            self.report({'ERROR'}, "Cubr is not enabled")
            return {'CANCELLED'}

        if not props.auth().is_user_logged_in:
            self.report({'ERROR'}, "You are not logged in")
            return {'CANCELLED'}

        if not props.props().render_active:
            self.report({'ERROR'}, "No render is active")
            return {'CANCELLED'}

        try:
            r = props.api().cancel_render(props.props().render_id)

            if r.status_code != 200:
                e = str(r.status_code) + r.text
                raise Exception("Cubr: Failed to cancel render: " + e)

            res = r.json()
            print("Cubr: Cancel render response: " + r.text)

            if "error" in res:
                raise Exception(
                    "Cubr: Failed to cancel render: " + res["message"])

            print("Cubr: Render cancelled")

            poll_render()

            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, "Failed to cancel render")
            print(e)
            return {'CANCELLED'}


def execute(self, context, is_animation: bool):
    if not props.is_addon_enabled:
        self.report({'ERROR'}, "Cubr is not enabled")
        return {'CANCELLED'}

    if not props.auth().is_user_logged_in:
        self.report({'ERROR'}, "You are not logged in")
        return {'CANCELLED'}

    p = props.props()

    output_path = bpy.context.scene.render.filepath
    output_dir = os.path.dirname(output_path)

    if not os.access(output_dir, os.W_OK):
        self.report(
            {'ERROR'}, "Output directory is not writable: " + output_dir)
        return {'CANCELLED'}

    if not os.path.isdir(output_dir):
        self.report({'ERROR'}, "Invalid output directory: " + output_dir)
        return {'CANCELLED'}

    if bpy.context.scene.render.image_settings.file_format != 'PNG' or p.render_file_format != 'PNG':
        self.report(
            {'ERROR'}, "Only PNG is supported. Contact us if you need another format.")
        return {'CANCELLED'}

    if bpy.context.scene.render.engine != 'CYCLES' or p.render_engine != 'CYCLES':
        self.report(
            {'ERROR'}, "Only Cycles is supported. Contact us if you need another engine.")
        return {'CANCELLED'}

    try:
        boost = 1
        if props.props().boost_enabled:
            boost = props.props().boost_amount

        r = None
        if is_animation:
            r = props.api().render_animation(
                props.props().file_id, boost, get_render_settings())
        else:
            r = props.api().render_still(props.props().file_id, boost, get_render_settings())

        if r.status_code != 200:
            self.report({'ERROR'}, "Failed to start render")
            print("Cubr: Failed to start render: " +
                  str(r.status_code) + r.text)
            return {'CANCELLED'}

        res = r.json()
        print("Cubr: Start render response: " + r.text)

        if "error" in res:
            self.report(
                {'ERROR'}, "Failed to start render: " + res["message"])
            print("Cubr: Failed to start render: " + res["message"])
            return {'CANCELLED'}

        print("Cubr: Rendering")

        p = props.props()

        p.render_animation = is_animation

        p.render_active = True
        p.render_id = res['render_id']
        p.render_file_id = props.props().file_id
        p.render_status = "Pending"
        p.render_progress = 0
        p.render_output_dir = output_dir
        p.render_output_name = os.path.basename(output_path)
        p.render_output_use_extension = bpy.context.scene.render.use_file_extension

        props.clear_last_render()

        p.last_render_id = p.render_id

        bpy.app.timers.register(poll_render)

        return {'FINISHED'}
    except Exception as e:
        self.report({'ERROR'}, "Failed to start render")
        print("Cubr: Failed to start render: " + str(e))
        props.clear_render()
        return {'CANCELLED'}


def get_render_settings():
    return {
        "engine": bpy.context.scene.render.engine,
        "frame_current": bpy.context.scene.frame_current,
        "frame_start": bpy.context.scene.frame_start,
        "frame_end": bpy.context.scene.frame_end,
        "frame_step": bpy.context.scene.frame_step,
        "noise_threshold": bpy.context.scene.cycles.adaptive_threshold,
        "samples": bpy.context.scene.cycles.samples,
        "min_samples": bpy.context.scene.cycles.adaptive_min_samples,
        "resolution_x": bpy.context.scene.render.resolution_x,
        "resolution_y": bpy.context.scene.render.resolution_y,
        "resolution_percentage": bpy.context.scene.render.resolution_percentage,
        "use_border": bpy.context.scene.render.use_border,
        "border_min_x": bpy.context.scene.render.border_min_x,
        "border_max_x": bpy.context.scene.render.border_max_x,
        "border_min_y": bpy.context.scene.render.border_min_y,
        "border_max_y": bpy.context.scene.render.border_max_y,
        "use_crop_to_border": bpy.context.scene.render.use_crop_to_border,
    }
