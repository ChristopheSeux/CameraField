import bpy
import random
from mathutils import Vector

from .functions import remap, draw_callback_3d


class ViewCameraField(bpy.types.Operator):
    bl_idname = "camerafield.view_field"
    bl_label = "Add Camera Frustum"
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Press escape to quit"

    def __init__(self):
        scene = bpy.context.scene
        self.current_frame = scene.frame_current

        cam = scene.camera

        ratio = bpy.context.scene.render.resolution_y / bpy.context.scene.render.resolution_x

        self.frames = {}
        tmp_frame = []

        self.rays = []
        self.border = []

        for i in range(scene.frame_start, scene.frame_end + 1):
            scene.frame_set(i)

            cam_coord = cam.matrix_world.to_translation()
            frame = cam.data.view_frame(bpy.context.scene)

            density = bpy.context.scene.camera_frustum_settings.density

            frame = [cam.matrix_world * corner for corner in frame]

            if frame != tmp_frame:
                tmp_frame = frame
                self.frames[i] = {}
                #self.frames[i]['border'] = []
                self.frames[i]['plain'] = []

                vector_x = Vector(frame[0]-frame[3])
                vector_y = Vector(frame[2]-frame[3])

                len_x = vector_x.length
                len_y = vector_y.length

                vector_x.normalize()
                vector_y.normalize()

                for z in range(0, density):
                    random_x = random.random()
                    random_y = random.random()
                    point = frame[3] + vector_x * random_x * len_x + vector_y * random_y * len_y

                    ray = bpy.context.scene.ray_cast(cam_coord, point - cam_coord, 8000)

                    if ray[0] :
                        ray_closer = ray[1] + (point-ray[1]).normalized() * 0.02
                        self.frames[i]['plain'].append(ray_closer)
                '''
                y_nb = round(density*ratio)
                for x in range(0,density+1):
                    for y in range (0,y_nb+1):
                        vector_x = Vector(frame[0]-frame[3])
                        vector_y = Vector(frame[2]-frame[3])

                        len_x = vector_x.length
                        len_y = vector_y.length

                        vector_x.normalize()
                        vector_y.normalize()

                        point = frame[3]+vector_x*remap(x,0,density,0,1)*len_x +vector_y*remap(y,0,y_nb,0,1)*len_y

                        ray = bpy.context.scene.ray_cast(cam_coord,point-cam_coord,8000)

                        #print(point,ray)

                        ray_closer = ray[1]+(point-ray[1]).normalized()*0.02

                        if ray[0] :

                            self.frames[i]['plain'].append(ray_closer)
                                '''
                    #self.frames[i]['border'] =[border_top,border_left,border_right,border_bottom]
                        #rays.append(bpy.context.scene.ray_cast(cam_coord,point_y-cam_coord,8000)[1])

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
