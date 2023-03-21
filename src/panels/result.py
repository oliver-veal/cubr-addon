import bpy

from .. import props


class PanelResult(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_cubr_result"
    bl_label = "Result"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cubr"

    def draw(self, context):
        if props.props() == None:
            return

        if not props.is_addon_enabled or not props.auth().is_user_logged_in:
            return

        layout = self.layout
        p = props.props()

        layout.use_property_split = True
        layout.use_property_decorate = False

        if p.last_render_id == "":
            return

        row = layout.row(align=True)
        if p.last_render_status == "canceled":
            row_alert = row.row(align=True)
            row_alert.alert = True
            row_alert.label(text="Canceled", icon="CANCEL")
        elif p.last_render_status == "failed":
            row_alert = row.row(align=True)
            row_alert.alert = True
            row_alert.label(text="Failed", icon="ERROR")
        elif p.last_render_status == "complete":
            row.label(text="Complete", icon="CHECKMARK")
        row.operator("cubr.open_render_dashboard", icon="URL", text="")

        grid = layout.grid_flow(columns=2, align=True)

        grid.label(text="Elapsed")
        row = grid.row(align=True)
        row.label(text=p.last_render_elapsed, icon="TIME")

        grid.label(text="Cost")
        row = grid.row(align=True)
        row.label(text=p.last_render_cost)

        if p.last_render_status == "complete":
            layout.separator()
            if p.last_render_animation:
                layout.operator("render.play_rendered_anim",
                                text="View Animation", icon="PLAY")
            else:
                layout.operator("cubr.view_show", icon="RESTRICT_VIEW_OFF")


def show_result_panel():
    if not hasattr(bpy.types, PanelResult.bl_idname):
        bpy.utils.register_class(PanelResult)


def hide_result_panel():
    if hasattr(bpy.types, PanelResult.bl_idname):
        bpy.utils.unregister_class(PanelResult)
