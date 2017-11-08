import bpy
import random
from math import sqrt
from mathutils import Vector

from .functions import draw_callback_3d


class ViewCameraField(bpy.types.Operator):
    bl_idname = "camerafield.view_field"
    bl_label = "Add Camera Frustum"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Press escape to quit"

    def __init__(self):
        scene = bpy.context.scene
        self.current_frame = scene.frame_current

        if scene.camera_frustum_settings.only_active:
            cams = (scene.camera,)
        else:
            cams = [o for o in bpy.context.visible_objects if o.type == 'CAMERA']

        ratio = bpy.context.scene.render.resolution_y / bpy.context.scene.render.resolution_x

        # self.frames = {}
        tmp_frame = []

        self.points = {"co": [],
                       "colors": []}

        for i in range(scene.frame_start, scene.frame_end + 1):
            scene.frame_set(i)
            random.seed(0)  # Use a predictable seed

            for cam in cams:
                cam_color = cam.data.camera_frustum_settings.color
                cam_coord = cam.matrix_world.to_translation()
                frame = cam.data.view_frame(scene)

                density = scene.camera_frustum_settings.density

                frame = [cam.matrix_world * corner for corner in frame]

                vector_x = frame[0] - frame[3]
                vector_y = frame[2] - frame[3]

                # for z in range(0, density):
                #     random_x = random.random()
                #     random_y = random.random()

                number_x = sqrt(density) / ratio
                number_y = sqrt(density) #* ratio

                for x in range(int(number_x)):
                    for y in range(int(number_y)):
                        point = (frame[3]
                                 + vector_x * x / (int(number_x) - 1)
                                 + vector_y * y / (int(number_y) - 1)
                                 )

                        ray = scene.ray_cast(cam_coord, point - cam_coord)

                        if ray[0]:
                            ray_closer = ray[1] + (point-ray[1]).normalized() * 0.02

                            point_color = cam_color.copy()
                            if i in (scene.frame_start, scene.frame_end):
                                point_color.s *= 0.5
                            if not ray_closer in self.points["co"]:
                                self.points["co"].append(ray_closer)
                                self.points["colors"].append(point_color)

    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type in {'ESC'}:
            bpy.types.SpaceView3D.draw_handler_remove(self._handle_3d, 'WINDOW')

            return {'CANCELLED'}

        return {'PASS_THROUGH'}
        #return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # the arguments we pass the the callback
            args = (self, context)
            # Add the region OpenGL drawing callback
            # draw in view space with 'POST_VIEW' and 'PRE_VIEW'
            self._handle_3d = bpy.types.SpaceView3D.draw_handler_add(draw_callback_3d, args, 'WINDOW', 'POST_VIEW')

            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}
