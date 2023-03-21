import bpy

from .. import props


class PanelRender(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_cubr_render"
    bl_label = "Render"
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

        if p.render_active:
            progress = layout.row(align=True)
            progress.operator(
                "cubr.open_render_dashboard",
                icon="URL",
                text=""
            )
            pr = progress.row()
            pr.enabled = False
            pr.prop(
                p,
                "render_progress",
                text="Progress", slider=True
            )
            progress.operator(
                "cubr.cancel_render", text="", icon="X"
            )

            grid = layout.grid_flow(columns=2, align=True)

            grid.label(text="Elapsed")
            grid.row().label(text=p.render_elapsed, icon="TIME")

            grid.label(text="Cost")
            grid.row().label(text=p.render_cost)
        else:
            layout.use_property_split = True
            layout.use_property_decorate = False

            draw_render_buttons(self, context)


def draw_render_buttons(self, context):
    enabled = props.is_addon_enabled and props.auth(
    ).is_user_logged_in and props.is_file_ready and not props.is_file_saving and not props.props().render_active

    layout = self.layout

    still = layout.row()
    still.enabled = enabled
    still.operator(
        "cubr.render_image",
        text="Cloud Render Image",
        icon="RENDER_STILL"
    )

    anim = layout.row()
    anim.enabled = enabled
    anim.operator(
        "cubr.render_animation",
        text="Cloud Render Animation",
        icon="RENDER_ANIMATION"
    )


def draw_view_button(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("cubr.view_show", text="View Cloud Render",
                    icon="RESTRICT_VIEW_OFF")
    layout.separator()


def draw_render_menu(self, context):
    draw_render_buttons(self, context)
    draw_view_button(self, context)


def show_render_panel():
    if not hasattr(bpy.types, PanelRender.bl_idname):
        bpy.utils.register_class(PanelRender)


def hide_render_panel():
    if hasattr(bpy.types, PanelRender.bl_idname):
        bpy.utils.unregister_class(PanelRender)
