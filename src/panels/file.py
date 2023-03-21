import bpy

from .. import props


class PanelFile(bpy.types.Panel):
    bl_idname = "VIEW3D_PT_cubr_file"
    bl_label = "File"
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

        if not bpy.data.use_autopack:
            row = layout.row()
            row.label(text="Autopack is disabled.")
            layout.operator("cubr.enable_autopack", text="Enable Autopack")
        else:
            # row = layout.row()
            # row.prop(bpy.data, "is_dirty")

            grid = layout.grid_flow(
                columns=2 if props.is_file_ready else 1, align=True)

            grid.label(text="Sync Status")
            row = grid.row()
            row.label(text=p.file_status, icon=props.props().file_status_icon)

            if props.is_file_ready:
                grid.label(text="Last Synced")
                row = grid.row()
                row.label(text=p.file_last_synced, icon="TIME")


def show_file_panel():
    if not hasattr(bpy.types, PanelFile.bl_idname):
        bpy.utils.register_class(PanelFile)


def hide_file_panel():
    if hasattr(bpy.types, PanelFile.bl_idname):
        bpy.utils.unregister_class(PanelFile)
