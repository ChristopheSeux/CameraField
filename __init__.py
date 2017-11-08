bl_info = {
    "name": "Camera Field",
    "author": "Christophe SEUX",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "description": "View camera frustum",
    "warning": "",
    "wiki_url": "",
    "category": "Camera",
    }


if "bpy" in locals():
    import imp
    imp.reload(operators)
    imp.reload(panels)

else:
    from .operators import *
    from .panels import *


class CameraFrustumSettings(bpy.types.PropertyGroup):
    density = bpy.props.IntProperty(default=2000,
                                    name='Density',
                                    description='Camera frustum point density')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.camera_frustum_settings = bpy.props.PointerProperty(type=CameraFrustumSettings)


def unregister():
    del bpy.types.Scene.camera_frustum_settings
    bpy.utils.unregister_module(__name__)
