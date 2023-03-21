import bpy

from .. import props


class PanelCubr(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_cubr_cubr"
    bl_label = "Cubr"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Cubr"

    def draw(self, context):
        layout = self.layout

        if not props.is_addon_enabled:
            layout.operator(
                "cubr.enable", text="Activate Cubr", icon="LINKED")
        else:
            p = props.props()

            if p is None:
                return

            if props.auth().is_user_logged_in:
                col = layout.column()
                row = col.row(align=True)
                row.operator("cubr.open_dashboard", icon="URL")
                row.operator("cubr.open_support", icon="QUESTION")
                col.operator("cubr.logout", icon="USER")
            else:
                if p.pairing_code == "":
                    layout.operator("cubr.login", text="Login", icon="USER")
                else:
                    row = layout.row()
                    row.label(text="Pairing code: " + p.pairing_code)
                    row.operator("cubr.cancel_login", text="", icon="X")


def draw_help_menu(self, context):
    layout = self.layout

    still = layout.row()
    still.operator(
        "cubr.open_support",
        text="Cubr: Support",
        icon="URL",
    )

    layout.separator()
