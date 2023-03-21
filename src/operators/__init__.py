import bpy

from .auth import OperatorLogin, OperatorCancelLogin, OperatorLogout
from .autopack import OperatorEnableAutopack
from .enable import OperatorEnable
from .render import OperatorRenderImage, OperatorRenderAnimation, OperatorCancelRender
from .view import OperatorView
from .dashboard import OperatorOpenSupport, OperatorOpenDashboard, OperatorOpenRenderInDashboard
from .info import OperatorInfo

CLASSES = [
    OperatorInfo,
    OperatorView,
    OperatorEnable,
    OperatorEnableAutopack,
    OperatorLogin,
    OperatorCancelLogin,
    OperatorLogout,
    OperatorRenderImage,
    OperatorRenderAnimation,
    OperatorCancelRender,
    OperatorOpenSupport,
    OperatorOpenDashboard,
    OperatorOpenRenderInDashboard,
]


def register():
    for cls in CLASSES:
        bpy.utils.register_class(cls)


def unregister():
    for cls in CLASSES:
        try:
            bpy.utils.unregister_class(cls)
        except:
            pass
