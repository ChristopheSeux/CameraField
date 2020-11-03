import bpy
import bgl
import gpu
from gpu_extras.batch import batch_for_shader

shader = gpu.shader.from_builtin('3D_FLAT_COLOR')

def draw_callback_3d(cameras):
    bgl.glPointSize(4)
    bgl.glEnable(bgl.GL_BLEND)

    coords = []
    colors = []

    for cam in cameras:
        if cam['camera_data'].camera_frustum_settings.enable:
            for co in cam["co"]:
                coords.append(co)
                colors.append(list(cam["color"]) + [0.5])

    batch = batch_for_shader(shader, 'POINTS', {"pos": coords,
                                                "color": colors})
    shader.bind()

    batch.draw(shader)

    # Restore opengl defaults
    bgl.glPointSize(1)
    bgl.glDisable(bgl.GL_BLEND)
