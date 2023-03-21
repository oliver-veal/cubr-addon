import bpy

from .cubr import PanelCubr, draw_help_menu
from .file import PanelFile
from .render import PanelRender, draw_render_menu
from .result import PanelResult

CLASSES = [
    PanelCubr,
]

UNREGISTER = [
    PanelFile,
    PanelRender,
    PanelResult,
] + CLASSES


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)

    bpy.types.TOPBAR_MT_help.prepend(draw_help_menu)
    bpy.types.TOPBAR_MT_render.prepend(draw_render_menu)


def unregister():
    for cls in UNREGISTER:
        if hasattr(bpy.types, cls.bl_idname):
            bpy.utils.unregister_class(cls)

    bpy.types.TOPBAR_MT_help.remove(draw_help_menu)
    bpy.types.TOPBAR_MT_render.remove(draw_render_menu)
